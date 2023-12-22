from django.shortcuts import render, redirect
from .models import Trade
from .forms import TradeForm
from django.views import View
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class HomeView(View):
    template_name = 'base.html'

    def get(self, request):
        if request.user.is_authenticated:
            # If the user is already authenticated, redirect to the home page
            return render(request, self.template_name)
        else:
            # If the user is not authenticated, redirect to the login page
            return redirect('account/login')


@login_required
@permission_required('your_app.delete_trade', raise_exception=True)
def delete_trade(request, trade_id):
    try:
        trade = Trade.objects.get(id=trade_id, user=request.user)
        deleted_row_number = trade.row_number  # Store the row number before deletion
        trade.delete()

        # After deletion, re-order the remaining rows
        remaining_trades = Trade.objects.filter(user=request.user).order_by('row_number')

        for index, remaining_trade in enumerate(remaining_trades, start=1):
            remaining_trade.row_number = index
            remaining_trade.save()

        return JsonResponse({'success': True, 'deleted_row_number': deleted_row_number})
    except Trade.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Trade not found or does not belong to the user'})

@login_required
def trade_list(request):
   
    
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
            

            return redirect('trade_list')

    else:
        form = TradeForm()
        
    # Filter trades based on the logged-in user
    trades = Trade.objects.filter(user=request.user).order_by('row_number')
    
        # Pagination
    paginator = Paginator(trades, 5)  # Show 5 trades per page
    page = request.GET.get('page')

    try:
        trades = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        trades = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        trades = paginator.page(paginator.num_pages)

    return render(request, 'trade_list.html', {'trades': trades, 'form': form})




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
