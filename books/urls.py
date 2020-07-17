from django.urls import path
from .views import *
from product.views import *
from .ajax import *

app_name = 'books'

urlpatterns = [
    path('', index, name='index'),
    path('login', login_view, name='login'),
    path('add/product', AddProduct.as_view(), name='add'),
    path('search_login', search_login, name='search_login'),
    path('add_provider', add_provider, name='add_provider'),
    path('download_providers', download_providers, name='download_providers'),
    path('search_subcategory', search_subcategory, name='search_subcategory'),
    path('page/<str:page_name>', page_views, name='page_views'),
    path('cart', cart_view, name='cart_view'),
 
]