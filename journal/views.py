from django.shortcuts import render, redirect
from .models import Trade
from .forms import TradeForm
from django.views import View
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


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
            trade.save()
            return redirect('trade_list')
    else:
        form = TradeForm()

    # Filter trades based on the logged-in user
    trades = Trade.objects.filter(user=request.user).order_by('row_number')

    return render(request, 'trade_list.html', {'trades': trades, 'form': form})

