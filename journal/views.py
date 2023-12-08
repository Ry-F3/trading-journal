from django.shortcuts import render, redirect
from .models import Trade
from .forms import TradeForm

def trade_list(request):
    trades = Trade.objects.all()
    return render(request, 'trade_list.html', {'trades': trades})

def add_trade(request):
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trade_list')
    else:
        form = TradeForm()
    return render(request, 'add_trade.html', {'form': form})
