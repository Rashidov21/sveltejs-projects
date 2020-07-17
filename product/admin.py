from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
	list_display = ['page_product_limit','alert_product_limit','system_sound','add_cart_product_count_0']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
	list_display = ['name','adres','contract_number','inn_number']