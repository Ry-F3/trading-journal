from django.shortcuts import render, redirect
from django.db.models import F
from .models import Trade
from .forms import TradeForm
from django.views import View
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from reportlab.lib.pagesizes import letter
from datetime import date 
from reportlab.pdfgen import canvas
from io import StringIO,  BytesIO
import csv


def get_trade_list(user, request):
    trades = Trade.objects.filter(user=user).order_by('row_number')
    paginator = Paginator(trades, 4)
    page = 1  # Default to the first page if not specified
    try:
        page = int(request.GET.get('page', 1))
        trades = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        trades = paginator.page(1)  # Display the first page if page is out of range
    return trades, paginator.num_pages, page


class HomeView(View):
    template_name = 'trade_list.html'

    def get(self, request):
        if request.user.is_authenticated:
            user_name = request.user.username 
            trades, last_page, current_page = get_trade_list(request.user, request)
            form = TradeForm()
            context = {'trades': trades, 'form': form, 'last_page': last_page, 'current_page': current_page, 'user_name': user_name}
            return render(request, self.template_name, context)
        else:
            return redirect('account/login')

    def post(self, request):
        # Handle POST request if needed
        return HttpResponse("POST request")



@login_required
def delete_trade(request, trade_id):
    try:
        trade = Trade.objects.get(id=trade_id, user=request.user)
        deleted_row_number = trade.row_number  # Store the row number before deletion
        trade.delete(request.user)  # Pass the user to the delete method

        # After deletion, re-order the remaining rows in a single query
        Trade.objects.filter(user=request.user, row_number__gt=deleted_row_number).update(
            row_number=F('row_number') - 1
        )

        return JsonResponse({'success': True, 'deleted_row_number': deleted_row_number})
    except Trade.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Trade not found or does not belong to the user'})



@login_required
def trade_list(request):
    user_name = request.user.username
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.user = request.user  # Set the user to the logged-in user
            save_type = request.POST.get('save_type', 'regular')
            
            if save_type == 'regular':
                # Save the trade as usual
                trade.save()
                # existing_trade.save()
                # Redirect to the same page to avoid reposting on refresh
                return HttpResponseRedirect(request.path)
                
            if save_type == 'overwrite':
                overwrite_id = request.POST.get('current_trade_id', None)
                overwrite_row = request.POST.get('current_row_number', None)

                #  # Get the form data
                edited_trade_data = {
                    'symbol': request.POST.get('symbol'),
                    'date': request.POST.get('date'),
                    'status': request.POST.get('status'),
                    'long_short': request.POST.get('long_short'),
                    'position': request.POST.get('position'),
                    'margin': request.POST.get('margin'),
                    'leverage': request.POST.get('leverage'),
                    'open_price': request.POST.get('open_price'),
                    'current_price': request.POST.get('current_price'),
                    'return_pnl': request.POST.get('return_pnl'),
                }
                
                # Print debugging information
                print(f"Overwrite ID: {overwrite_id}, Row: {overwrite_row}")
                print("Edited Trade Data:", edited_trade_data)

                if overwrite_id is not None and overwrite_row is not None:
                    # Your overwrite logic here
                    trade.save_overwrite(overwrite_id=overwrite_id, overwrite_row=overwrite_row, edited_trade_data=edited_trade_data)
                else:
                    # Your regular save logic here
                    trade.save()

        else:
            

            return render(request, 'trade_list.html', {'trades': trades, 'form': form, 'user_name': user_name})

    else:
        form = TradeForm()
        
    

    # Filter trades based on the logged-in user
    trades = Trade.objects.filter(user=request.user).order_by('row_number')
    
      # Pagination
    paginator = Paginator(trades, 4)  # Show 5 trades per page
    page = request.GET.get('page')

    # Determine the last page dynamically
    last_page = paginator.num_pages

    try:
        # If page is not an integer, deliver last page.
        trades = paginator.page(page)
    except PageNotAnInteger:
        trades = paginator.page(last_page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        trades = paginator.page(last_page)

    # If no specific page parameter is provided, redirect to the last page
    if not page:
        return render(request, 'trade_list.html', {'trades': trades, 'form': form, 'user_name': user_name})
   

    return render(request, 'trade_list.html', {'trades': trades, 'form': form, 'user_name': user_name})




@login_required
def get_trade_details(request, row_number, trade_id):
    try:
        # Print row_number and trade_id for debugging purposes
        print(f"Row Number: {row_number}, Trade ID: {trade_id}")
        
        trade = Trade.objects.get(row_number=row_number, id=trade_id, user=request.user)
        trade_details = {
            'symbol': str(trade.symbol),
            'date': str(trade.date),
            'status': str(trade.status),
            'long_short': str(trade.long_short),
            'position': trade.position,
            'margin': trade.margin,
            'leverage': trade.leverage,
            'open_price': trade.open_price,
            'current_price': trade.current_price,
            'return_pnl': trade.return_pnl,
           
        }
        
        return JsonResponse({'success': True, 'trade_details': trade_details})
    except Trade.DoesNotExist as e:
        print(f"Error: {e}")
        return JsonResponse({'success': False, 'error': 'Trade not found or does not belong to the user'})
 

def generate_pdf_report(user, trades):
    # Create a PDF with trade data
    pdf_buffer = BytesIO()
    p = canvas.Canvas(pdf_buffer, pagesize=letter)
    
    # Title and date
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 770, f'Trade Report ')  # Adjusted x-coordinate
    p.setFont("Helvetica", 10)
    today = date.today().strftime("%Y-%m-%d")
    p.drawString(50, 750, f"Date: {today}")  # Adjusted x-coordinate
    # User information (adjusted x and y coordinates)
    p.setFont("Helvetica", 10)
    p.drawString(50, 730, f"Username: {user.username}")

    # Content
    p.setFont("Helvetica", 7)
    y_position = 720
    for trade in trades:
        y_position -= 15
        x_position = 50  # Adjusted x-coordinate
        trade_info = f"ID: {trade.id}, Symbol: {trade.symbol}, Date: {trade.date}, Status: {trade.status}, " \
                     f"Long/Short: {trade.long_short}, Margin: {trade.margin}, " \
                     f"Leverage: {trade.leverage}, Open Price: {trade.open_price}, " \
                     f"Current Price: {trade.current_price}, Return PNL: {trade.return_pnl}"
        p.drawString(x_position, y_position, trade_info)

    p.showPage()
    p.save()

    pdf_buffer.seek(0)
    pdf_data = pdf_buffer.getvalue()
    pdf_buffer.close()

    return pdf_data


def generate_report(request): # Can be used for other file types if needed in the future e.g csv
    if request.user.is_authenticated:
        user = request.user
        trades = Trade.objects.filter(user=user).order_by('row_number')

        # Choose either CSV or PDF
        report_format = request.GET.get('format', 'csv')

        if report_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="trade_report.csv"'
            csv_data = generate_csv_report(trades)
            response.write(csv_data)
            return response
        elif report_format == 'pdf':
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="trade_report.pdf"'
            pdf_data = generate_pdf_report(user, trades)
            response.write(pdf_data)
            return response
        else:
            # Handle unsupported format
            return HttpResponse("Unsupported format")
    else:
        return redirect('account/login')