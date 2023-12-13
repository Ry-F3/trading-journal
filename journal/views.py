from django.shortcuts import render, redirect
from .models import Trade
from .forms import TradeForm
from django.views import View

def trade_list(request):
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the same page after form submission to refresh the data
            return redirect('trade_list')
    else:
        form = TradeForm()

    trades = Trade.objects.all()

    return render(request, 'trade_list.html', {'trades': trades, 'form': form})

class HomeView(View):
    template_name = 'base.html'

    def get(self, request):
        if request.user.is_authenticated:
            # If the user is already authenticated, redirect to the home page
            return render(request, self.template_name)
        else:
            # If the user is not authenticated, redirect to the login page
            return redirect('account/login')

