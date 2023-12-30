from django.shortcuts import render, redirect
from django.db.models import F
from .models import Trade, UserProfile, PortfolioHistory
from .forms import TradeForm, PortfolioBalanceForm
from django.views import View
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from reportlab.lib.pagesizes import letter
from datetime import date, timedelta 
from reportlab.pdfgen import canvas
from io import StringIO,  BytesIO
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, HourLocator
import matplotlib.dates as mdates
import base64
from decimal import Decimal


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
    home = 'trade_list.html'

    def get(self, request):
        if request.user.is_authenticated:
            time_interval = request.GET.get('time_interval', 'hourly')
            user_name = request.user.username 
            trades, last_page, current_page = get_trade_list(request.user, request)
            form = TradeForm()
            context = {'trades': trades, 'form': form, 'last_page': last_page, 'current_page': current_page, 'user_name': user_name, 'time_interval': time_interval,   'image_base64': image_base64,}
            return render(request, self.home, context)
        else:
            return redirect('account/login')

    def post(self, request):
        # Handle POST request if needed
        return HttpResponse("POST request")
    

class BlogView(View):
    blog = 'blog.html' 

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_name = request.user.username 
            context = {'user_name': user_name}
        return render(request, self.blog, context)
    

class ContactView(View):
    contact = 'contact.html' 

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_name = request.user.username 
            context = {'user_name': user_name}
        return render(request, self.contact, context)
    

@login_required
def delete_trade(request, trade_id):
    try:
        trade = Trade.objects.get(id=trade_id, user=request.user)
        time_interval = request.GET.get('time_interval', 'hourly')
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
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    image_base64 = plot_realized_profits_chart(request)  # Initialize the chart
    portfolio_balance = user_profile.portfolio_balance  # Initialize with the current portfolio balance
    
    # Handle Portfolio Balance Form Submission
    if request.method == 'POST':
        portfolio_balance_form = PortfolioBalanceForm(request.POST)
        if portfolio_balance_form.is_valid():
            # Process the portfolio balance form data and update the model instance
            update_amount = portfolio_balance_form.cleaned_data['portfolio_balance']
            action = request.POST.get('action')

            # Determine whether to add or subtract based on the button clicked
            if action == 'add':
                user_profile.portfolio_balance += update_amount
            elif action == 'subtract':
                user_profile.portfolio_balance -= update_amount

            # Save the updated portfolio balance
            user_profile.save()

            # Calculate PnL only if the form is valid
            pnl_data = calculate_pnl(request.user)

            print('PnL Calculation Result:', pnl_data)  # Add this line for debugging purposes
            print('Portfolio Balance after PnL Calculation:', user_profile.portfolio_balance)  # Add this line for debugging purposes

            # Redirect to the same page to avoid reposting on refresh
            return HttpResponseRedirect(request.path)
    else:
        portfolio_balance_form = PortfolioBalanceForm()
        print('Not a POST request. Portfolio Balance Form:', portfolio_balance_form)  # Add this line for debugging purposes
        
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.user = request.user  # Set the user to the logged-in user
            save_type = request.POST.get('save_type', 'regular')
            
            if save_type == 'regular':
                # Save the trade as usual
                trade.save()
                
                 # Retrieve or create the UserProfile associated with the logged-in user
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.portfolio_balance = portfolio_balance
                user_profile.save()

                # Calculate PnL only if the form is valid
                pnl_data = calculate_pnl(request.user)
                print('pnl:', pnl_data)
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
            
            return render(request, 'trade_list.html', {
                'trades': trades,
                'form': form,
                'portfolio_balance_form': portfolio_balance_form,
                'pnl_data': pnl_data,
                'user_name': user_name,
                'image_base64': image_base64,
                'time_interval': time_interval
            })

    else:
        form = TradeForm()
        
    # Filter trades based on the logged-in user
    trades = Trade.objects.filter(user=request.user).order_by('row_number')
    
    # Calculate PnL
    pnl_data = calculate_pnl(request.user)
    total_realized_pnl = pnl_data['total_realized_pnl']  # Capture the value
    
  
    
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
        time_interval = request.GET.get('time_interval', 'hourly')
        return render(request, 'trade_list.html', {
            'trades': trades,
            'form': form,
            'portfolio_balance_form': portfolio_balance_form,
            'pnl_data': pnl_data,
            'user_name': user_name,
            'image_base64': image_base64,
            'time_interval': time_interval
        })
   

    return render(request, 'trade_list.html', {
        'trades': trades,
        'form': form,
        'portfolio_balance_form': portfolio_balance_form,
        'pnl_data': pnl_data,
        'user_name': user_name,
        'image_base64': image_base64,
        'time_interval': time_interval
    })
    
def plot_realized_profits_chart(request):
    # Extract timestamps and realized profits
    timestamps = []
    realized_profits = []

    # Retrieve historical data
    history_data = PortfolioHistory.objects.filter(user=request.user).order_by('timestamp')

    # Populate timestamps and realized_profits
    for entry in history_data:
        timestamps.append(entry.timestamp)
        realized_profits.append(float(entry.total_realized_pnl))

    # Get the time interval from the URL parameter (default to 'hourly')
    time_interval = request.GET.get('time_interval', 'hourly')

    # Calculate time intervals based on user choice
    if time_interval == 'hourly':
        x_values = timestamps
        x_label = 'Time'
        x_format = '%H:%M:%S'
        interval_delta = timedelta(hours=1)
        # Set the locator and formatter for hourly ticks
        locator = HourLocator(interval=4)  # Adjust interval to display fewer hourly ticks
        formatter = DateFormatter(x_format)
    elif time_interval == 'daily':
        x_values = [timestamp.strftime('%Y-%m-%d') for timestamp in timestamps]
        x_label = 'Date'
        x_format = '%Y-%m-%d'
        interval_delta = timedelta(days=1)
    elif time_interval == 'monthly':
        x_values = [timestamp.strftime('%Y-%m') for timestamp in timestamps]
        x_label = 'Month'
        x_format = '%Y-%m'
        interval_delta = timedelta(days=30)
    elif time_interval == 'yearly':
        x_values = [timestamp.strftime('%Y') for timestamp in timestamps]
        x_label = 'Year'
        x_format = '%Y'
        interval_delta = timedelta(days=365)
    else:
        x_values = [timestamp.strftime('%H:%M:%S') for timestamp in timestamps]  # Default to hourly
        x_label = 'Time'
        x_format = '%H:%M:%S'
        interval_delta = timedelta(hours=1)

    # Plot the chart with a line connecting data points
    plt.plot(x_values, realized_profits, linestyle='-', color='#0d6efd')

    # Customize chart appearance
    plt.gcf().set_size_inches(10, 6)  # Set the size of the figure
    plt.xlabel(x_label, fontsize=22)  # Set X-axis label and font size
    plt.ylabel('Realized Profit', fontsize=22)  # Set Y-axis label and font size
    plt.title(f'Realized Profit Over {x_label}', fontsize=22)  # Set chart title and font size
    plt.grid(True)  # Add grid lines
    plt.legend(['Realized Profits'], loc='upper left')  # Add legend

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Encode the image to base64 for HTML embedding
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return image_base64


def calculate_pnl(user):
    # Fetch closed trades, open trades, and calculate PnL
    closed_trades = Trade.objects.filter(user=user, status='closed')
    open_trades = Trade.objects.filter(user=user, status='open')

    # Convert return_pnl values to Decimal
    closed_returns = [Decimal(trade.return_pnl) for trade in closed_trades]
    open_returns = [Decimal(trade.return_pnl) for trade in open_trades]

    # Calculate total realized PnL
    total_realized_pnl = sum(closed_returns)

    # Calculate total unrealized PnL
    total_unrealized_pnl = calculate_unrealized_pnl(open_returns)

    # Update UserProfile with total_realized_pnl
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    # Print debugging information
    print('Before Update - Portfolio Balance:', user_profile.portfolio_balance)
    print('Before Update - Total Realized PnL:', user_profile.total_realized_pnl)
    print('Before Update - Last Realized PnL:', user_profile.last_realized_pnl)

    # Calculate the change in realized profit since the last update
    realized_pnl_change = total_realized_pnl - user_profile.last_realized_pnl

    # Update total_realized_pnl only if there is a positive change
    if realized_pnl_change > 0:
        user_profile.total_realized_pnl = total_realized_pnl
        
    # Update portfolio_balance with the negative value if there are losses
    if realized_pnl_change < 0:
        user_profile.portfolio_balance -= abs(realized_pnl_change)

    # Update portfolio_balance only if there is a positive change
    if realized_pnl_change > 0:
        user_profile.portfolio_balance += realized_pnl_change
        print('Total Realized PnL Change:', realized_pnl_change)
        print('After Update - Portfolio Balance:', user_profile.portfolio_balance)

    # Update last_realized_pnl with the current total_realized_pnl
    user_profile.last_realized_pnl = total_realized_pnl
    user_profile.save()
    
     # Create a new PortfolioHistory entry
    portfolio_history_entry = PortfolioHistory.objects.create(
        user=user,
        total_realized_pnl=total_realized_pnl
    )


    return {
        'total_realized_pnl': total_realized_pnl,
        'total_unrealized_pnl': total_unrealized_pnl,
    }

def calculate_unrealized_pnl(open_returns):
    # Logic for calculating unrealized PnL from open trades
    # Separate positive and negative returns
    positive_returns = [return_pnl for return_pnl in open_returns if return_pnl > 0]
    negative_returns = [return_pnl for return_pnl in open_returns if return_pnl < 0]

    # Debug prints
    print("Calculate Unrealized PnL - Debug Prints:")
    print("Positive Returns:", positive_returns)
    print("Negative Returns:", negative_returns)

    # Calculate total unrealized PnL
    total_positive_pnl = sum(positive_returns)
    total_negative_pnl = sum(negative_returns)
    total_unrealized_pnl = total_positive_pnl + total_negative_pnl

    # Debug prints
    print("Total Unrealized PnL:", total_unrealized_pnl)

    return total_unrealized_pnl


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
    
