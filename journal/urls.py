from . import views
from django.urls import path
from .views import trade_list, delete_trade, get_trade_details, generate_report, ContactView, BlogView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('trade_list/', trade_list, name='trade_list'),
    path('trade_list/post/', trade_list, name='trade_list_post'),
    path('delete-trade/<int:trade_id>/', delete_trade, name='delete_trade'),
    path('generate_report/', generate_report, name='generate_report'),
    path('get_trade_details/<int:trade_id>/<int:row_number>/', views.get_trade_details, name='get_trade_details'),
 
]