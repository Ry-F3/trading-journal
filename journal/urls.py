from django.urls import path
from .views import trade_list, add_trade

urlpatterns = [
    path('trades/', trade_list, name='trade_list'),
    path('add_trade/', add_trade, name='add_trade'),
    # Add a pattern for the root path
    path('', trade_list, name='home'),  # 'trade_list' is the view for the home page
]