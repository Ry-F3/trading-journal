from django.shortcuts import render, redirect
from .models import Trade
from .forms import TradeForm
from django.db import models
from django.views import View
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

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
            trade.save()

            # Fetch the updated list of trades
            trades = Trade.objects.filter(user=request.user).order_by('row_number')
            trade_data = get_trade_data(trades)

            return JsonResponse({'success': True, 'trade_data': trade_data})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid form data'})
    else:
        form = TradeForm()

    # Filter trades based on the logged-in user
    trades = Trade.objects.filter(user=request.user).order_by('row_number')
    trade_data = get_trade_data(trades)

    return render(request, 'trade_list.html', {'trades': trades, 'form': form, 'trade_data': trade_data})

def get_trade_data(trades):
    trade_data = []
    for trade in trades:
        trade_data.append({
            'symbol': trade.symbol,
            'date': trade.date,
            'status': trade.status,
            'long_short': trade.long_short,
            'position': str(trade.position),
            'margin': str(trade.margin),
            'leverage': str(trade.leverage),
            'open_price': str(trade.open_price),
            'current_price': str(trade.current_price),
            'return_pnl': str(trade.return_pnl),
        })
    return trade_data


def get_trade_details_by_row(request, row_number):
    try:
        trade = Trade.objects.get(row_number=row_number, user=request.user)
        trade_details = {
            'symbol': trade.symbol,
            'date': trade.date,
            'status': trade.status,
            'long_short': trade.long_short,
            'position': str(trade.position),
            'margin': str(trade.margin),
            'leverage': str(trade.leverage),
            'open_price': str(trade.open_price),
            'current_price': str(trade.current_price),
            'return_pnl': str(trade.return_pnl),
            # Add other fields as needed
        }
        return JsonResponse({'success': True, 'trade_details': trade_details})
    except Trade.DoesNotExist as e:
        print(f"Error: {e}")
        return JsonResponse({'success': False, 'error': 'Trade not found or does not belong to the user'})

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetNextRowNumberView(View):
    def get(self, request, *args, **kwargs):
        try:
            # Get the maximum row number from the Trade model
            max_row_number = Trade.objects.aggregate(models.Max('row_number'))['row_number__max']
            next_row_number = int(max_row_number or 0) + 1
            print('plus 1')
        except Exception as e:
            # If an exception occurs (e.g., if there are no rows in the database),
            # set next_row_number to 1
            next_row_number = Trade.objects.count() + 1
            print(f"No rows found. Setting next_row_number to 1. Error: {e}")

        return JsonResponse({'success': True, 'next_row_number': next_row_number})




class HomeView(View):
    template_name = 'base.html'

    def get(self, request):
        if request.user.is_authenticated:
            # If the user is already authenticated, redirect to the home page
            return render(request, self.template_name)
        else:
            # If the user is not authenticated, redirect to the login page
            return redirect('account/login')
