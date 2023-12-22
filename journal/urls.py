from . import views
from django.urls import path
from .views import trade_list, delete_trade, get_trade_details

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('trade_list/', trade_list, name='trade_list'),
    path('trade_list/post/', trade_list, name='trade_list_post'),
    # path('test/', views.test_view, name='test'),
    path('delete-trade/<int:trade_id>/', delete_trade, name='delete_trade'),
    path('get_trade_details/<int:trade_id>/<int:row_number>/', views.get_trade_details, name='get_trade_details'),
 
]