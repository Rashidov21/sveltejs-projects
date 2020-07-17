from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
	list_display = ['user','position','name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['title']

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
	list_display = ['category','title']	

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['category','subcategory','title','quantity','date']


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
	list_display = ['name','adres','phone','contract_number']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
	list_display = ['product','qty','item_total']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ['id','cart_total']
						