
from . import views
from django.urls import path
from .views_blog import BlogView, search_trade, get_trade_details, view_post, like_toggle
from .views import (
    HomeView,
    ContactView,
    TradeFilterView,
    trade_list,
    delete_trade,
    get_trade_details,
    generate_report,
    update_portfolio_balance,
    get_portfolio_balance,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('trade_list/', TradeFilterView.as_view(), name='trade_list'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('search_trade/', search_trade, name='search_trade'),
    path('like_toggle/', like_toggle, name='like_toggle'),
    path('trade_list/', trade_list, name='trade_list'),
    path('update_portfolio_balance/', update_portfolio_balance, name='update_portfolio_balance'),
    path('trade_list/post/', trade_list, name='trade_list_post'),
    path('delete-trade/<int:trade_id>/', delete_trade, name='delete_trade'),
    path('generate_report/', generate_report, name='generate_report'),
    path('get_portfolio_balance/', get_portfolio_balance, name='get_portfolio_balance'),
    path('get_trade_details/<int:trade_id>/<int:row_number>/', get_trade_details, name='get_trade_details'),
    path('view_post/<int:post_id>/', view_post, name='view_post'),  # New URL for viewing individual posts
    # path('blog/', blog_post_list, name='blog_post_list'),
    # path('blog/<int:post_id>/', blog_post_detail, name='blog_post_detail'),
]


