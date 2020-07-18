from django.db import models

# Create your models here.

class Settings(models.Model):
	page_product_limit  = models.PositiveIntegerField("Tovar soni(1 page)",default=30,blank=True)
	alert_product_limit  = models.PositiveIntegerField("Ogoxlantirish (Kam qolgan tovar)",default=5,blank=True)
	system_sound = models.BooleanField("Sound",default=True)
	add_cart_product_count_0 = models.BooleanField("Savatchaga qo'shish (Product 0 dona)",default=False)
	color_product_limit = models.BooleanField("Oz qolgan tovarlar rang bilan ajratilsin",default=True)
	view_products_count_no = models.BooleanField("Omborda tugagan tovarlar ko'rsatilsin",default=True)
	view_products_check_no = models.BooleanField("Tekshirilmagan tovarlar ko'rsatilsin",default=True)
	add_products_for_one_provider_at_one_day_with_one_list = models.BooleanField("1kun ich. 1ta provider",default=True)


class Client(models.Model):
	name = models.CharField("Nomi", max_length=75)
	adres = models.CharField("Manzili", max_length=350)
	phone = models.CharField("Telefon", max_length=16,blank=True)
	contract_number = models.CharField("Shartnoma raqami", max_length=45,blank=True)
	inn_number = models.CharField("IIN", max_length=35,blank=True)
	reg_code = models.CharField("Registratsiya kodi", max_length=35,blank=True)
	director = models.CharField("Direktor", max_length=45,blank=True)
	counter = models.CharField("Xisobchi", max_length=45,blank=True)
	add_date = models.DateTimeField(auto_now_add=True)
	status = models.BooleanField(default=True)

	class Meta:
		ordering = ['-id']