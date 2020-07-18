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
    path('edit_product', edit_product, name='edit_product'),
    path('edit', edit_info_product, name='edit_info_product'),
    path('delivery-list', Delivery.as_view(), name='delivery'),
    path('delivery-product-list/<int:delivery_id>', delivery_products, name='delivery_product_list'),
    path('admin_order_pdf', admin_order_pdf, name='admin_order_pdf'),
    path('print/list/<int:delivery_id>', print_me, name='print_me'),
    path('send/list/pdf', send_add_pdf, name='send_add_pdf'),
 
]