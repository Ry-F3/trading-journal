from . import views
from django.urls import path
from django.db import models
from .views import trade_list, delete_trade, get_trade_details_by_row, GetNextRowNumberView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('trade_list/', trade_list, name='trade_list'),
    path('trade_list/post/', trade_list, name='trade_list_post'),
    path('delete-trade/<int:trade_id>/', delete_trade, name='delete_trade'),
    path('get_trade_details_by_row/<slug:row_number>/', views.get_trade_details_by_row, name='get_trade_details_by_row'),
    path('get_next_row_number/', GetNextRowNumberView.as_view(), name='get_next_row_number'),



]
