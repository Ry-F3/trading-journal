from . import views
from django.urls import path
from .views import trade_list

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('trade_list/', trade_list, name='trade_list'),
   
]
