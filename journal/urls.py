from . import views
from django.urls import path
from .views import trade_list, delete_trade

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('trade_list/', trade_list, name='trade_list'),
    path('trade_list/post/', trade_list, name='trade_list_post'),
     path('delete-trade/<int:trade_id>/', delete_trade, name='delete_trade'),
   
]
