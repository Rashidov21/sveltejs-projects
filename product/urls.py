from django.contrib import admin
from django.urls import path, include
from .views import *
from .ajax import *

app_name = 'product'

urlpatterns = [ 

    path('archive', ArchiveAddProduct.as_view(), name="products" ),
    path('search/date', search_date, name="search_date" ),
    path('add_to_cart', add_to_cart_view, name="add_to_cart" ),
    path('change_item_qty', change_item_qty, name="change_item_qty" ),
    path('remove_from_cart_view', remove_from_cart_view, name="remove_from_cart_view" ),
    path('loading_cart', loading_cart, name="loading_cart" ),
    path('control_price', control_price, name="control_price" ),
    path('reset_cart', reset_cart, name="reset_cart" ),
    path('catalog/<int:catalog_id>', catalog_view, name="catalog_view" ),
    path('dynamic/catalog', dynamic_catalog, name="dynamic_catalog" ),
    path('invoice', invoice, name="invoice" ),
    path('add_client', add_client, name="add_client" ),
    path('search_product', search_product, name="search_product" ),
    path('toprint/<int:client_id>', toprint, name="toprint" ),
    path('check', check_products, name="check_products" ),

]