from django.db import models
from django.urls import reverse
from django.conf import settings
from product.models import Settings


def image_folder(instance, filename):
	filename = instance.title +'.'+filename.split('.')[1]
	return"{0}/{1}".format(instance.title, filename)

def pdf_uploader(instance, filename):
	formate = filename.split('.')[1]
	filename = "{0}_{1}_{2}_{3}.{4}".format(instance.provider.name,instance.day,instance.month,instance.year,formate)
	return filename	


class Position(models.Model):
	name = models.CharField("Lavozim", max_length=50)
	def __str__(self):
		return self.name

class UserAccount(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
	position = models.ForeignKey(Position,on_delete=models.PROTECT,null=True, blank=True)
	name = models.CharField('Ismi',max_length=25)
	telegram_id = models.PositiveIntegerField(default=0,blank=True)
	last_name = models.CharField('Familyasi',max_length=25)
	adres = models.CharField(max_length=355,blank=True)
	info = models.TextField(max_length=555,blank=True)
	email = models.CharField(max_length=55,blank=True)
	phone = models.CharField(max_length=16)
	reg = models.DateTimeField(auto_now_add=True)
	status = models.BooleanField(default=True)

	def __str__(self):
		return "{0} {1}".format(self.name,self.last_name)




# Create your models here.
class Category(models.Model):
	title = models.CharField('Kategoriya nomi',max_length = 50)
	image = models.FileField('Foto Shart emas...',upload_to=image_folder, blank=True)


	

	class Meta:
		verbose_name = 'Kategoriya'
		verbose_name_plural = 'Kategoriyalar'

	def __str__(self):
		return "{}".format(self.title)	


class SubCategory(models.Model):
	category =  models.ForeignKey(Category, on_delete = models.CASCADE, verbose_name="Kategoriya *")	
	title = models.CharField('SubKategoriya nomi *',max_length=50)
	image = models.FileField('Foto Shart emas...',upload_to=image_folder, blank=True)
	

	class Meta:
		verbose_name = 'SubKategoriya'
		verbose_name_plural = 'SubKategoriyalar'

	def __str__(self):
		return "{}".format(self.title)
	
	# def get_absolute_url(self):
	# 	return reverse ('mynews:category_view', kwargs={'category_slug':self.slug})
class Provider(models.Model):
	name = models.CharField("Nomi", max_length=50)
	adres = models.CharField("Manzil", max_length=50)
	phone = models.CharField("Telefon raqam",blank=True, max_length=50)
	director = models.CharField("Direktor",blank=True, max_length=50)
	staff = models.CharField("Xodim",blank=True, max_length=50)
	contract_number = models.CharField("Shartnoma raqami",blank=True, max_length=50)
	inn = models.CharField("IIN raqami",blank=True, max_length=50)
	reg_code = models.CharField("Registratsiya kodi",blank=True, max_length=50)

	def __str__(self):
		return "{}".format(self.name)

class KeyWord(models.Model):
	key = models.CharField("Kalit so'z", max_length=350)
	date = models.CharField("Sana", max_length=50)
	qty = models.PositiveIntegerField('Soni',default=0,blank=True)
	user =  models.ForeignKey(UserAccount, on_delete = models.CASCADE,blank=True,null=True, verbose_name="Mas'ul")	
	summa = models.PositiveIntegerField('Summa',default=0,blank=True)
	status = models.BooleanField(default=True)

	def __str__(self):
		return self.key



class Product(models.Model):
	category = models.ForeignKey(Category, on_delete = models.CASCADE,verbose_name='Kategoriyasi')		
	subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, verbose_name="SubKategoriya ",blank=True, null=True)		
	added_by = models.ForeignKey(UserAccount,related_name = 'added_by', on_delete=models.PROTECT, verbose_name="Qo'shdi",blank=True, null=True)		
	check_by = models.ForeignKey(UserAccount,related_name = 'check_by', on_delete=models.PROTECT, verbose_name="Tekshirdi",blank=True, null=True)		
	key = models.ForeignKey(KeyWord,related_name = 'keyword', on_delete=models.PROTECT, verbose_name="Kalit so'z",blank=True, null=True)		
	title = models.CharField('Tovar nomi',max_length=40)
	author = models.CharField("Muallif",blank=True, max_length=80)
	edition = models.CharField("Nashriyot",blank=True, max_length=80)
	month = models.CharField("Oy",blank=True, max_length=15)
	date = models.CharField("Sana",blank=True, max_length=12)
	provider = models.ForeignKey(Provider,on_delete = models.CASCADE,verbose_name='Yetqazib beruvchi',blank=True, null=True)
	description = models.TextField('Tovar haqida',max_length=350,blank=True)
	image = models.ImageField('Foto Shart emas...',upload_to=image_folder,blank=True)
	quantity = models.PositiveIntegerField('Ombordagi soni',default=0)
	count_order = models.PositiveIntegerField('Sotilishlar soni',default=0, blank=True)
	pur_price = models.PositiveIntegerField('Olingan narxi',default=0,blank=True)
	cur_price = models.PositiveIntegerField('Sotiladigan narxi',default=0,blank=True)
	active = models.BooleanField(default=True)
	check = models.BooleanField(default=False)
	add_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)


	class Meta:
		verbose_name = 'Tovar'
		verbose_name_plural = 'Tovarlar'
		ordering = ["-id"]

	def __str__(self):
		return "{}".format(self.title)

	# def get_absolute_url(self):
	# 	return reverse ('product_url', kwargs={'product_id':self.id})



class AddProductArchive(models.Model):
	provider = models.ForeignKey(Provider,on_delete = models.PROTECT,verbose_name='Yetqazib beruvchi')
	check_by = models.ForeignKey(UserAccount, on_delete=models.PROTECT, verbose_name="Qo'shdi",blank=True, null=True)		
	product = models.ManyToManyField(Product, blank=True)
	year = models.PositiveIntegerField('Yil',default=2020)
	month = models.CharField("Oy",blank=True, max_length=12)
	day = models.PositiveIntegerField('Kun',default=0)
	quantity = models.PositiveIntegerField('Soni',default=0)
	summa = models.PositiveIntegerField('Summa',default=0)
	add_date = models.DateTimeField(auto_now_add=True)
	pdf = models.FileField(upload_to=pdf_uploader,blank=True)
	send_bot = models.BooleanField(default=False)
	save_as_folder = models.BooleanField(default=False)

	class Meta:
		ordering = ['-id']




class CartItem(models.Model):
	product = models.ForeignKey(Product,verbose_name='Tovar', on_delete=models.CASCADE)
	price = models.PositiveIntegerField("Narxi",default=0,blank=True)
	qty = models.PositiveIntegerField("Soni",default=1)
	item_total = models.PositiveIntegerField("Umumiy narxi",default=1)

	class Meta:
		verbose_name = 'Savatchadagi tovar'
		verbose_name_plural = 'Savatchadagi tovarlar'
		ordering = ["-id"]

	def __str__(self):
		return "Cart item for product {0}".format(self.product.title)

class Cart(models.Model):
	items = models.ManyToManyField(CartItem, blank=True)
	cart_total = models.PositiveIntegerField("Umumiy summa",default=0)
	all_qty = models.PositiveIntegerField("Umumiy tovarlar soni",default=0,blank=True)

	def __str__(self):
		return str(self.id)

	class Meta:
		verbose_name = 'Savatcha'
		verbose_name_plural = 'Savatchalar'
		ordering = ["-id"]	

	def add_to_cart(self, product_id):
		cart = self
		setting = Settings.objects.latest('-id')
		product = Product.objects.get(id=product_id)
		if product.quantity == 0:
			if setting.add_cart_product_count_0:
				pass
			else:	
				return 'No product'
		else:			
			new_item, _ = CartItem.objects.get_or_create(product=product,price=product.cur_price, item_total=product.cur_price)
	
			if new_item not in cart.items.all():
				cart.items.add(new_item)
				cart.all_qty += new_item.qty
				cart.save()

			else:
				return "Added"		

	def remove_from_cart(self, product_id):
		cart = self
		product = Product.objects.get(id=product_id)
		for cart_item in cart.items.all():
			if cart_item.product == product:
				cart.items.remove(cart_item)
				cart.save()	
		d = []
		for b in cart.items.all():
			d.append(b.qty)
		cart.all_qty = int(sum(d))		
		cart.save()	

	def change_qty(self, qty, item_id):
		cart = self
		cart_item = CartItem.objects.get(id=int(item_id))
		setting = Settings.objects.latest('-id')
		product = cart_item.product
		if product.quantity == 0:
			if setting.add_cart_product_count_0:
				pass
			else:	
				return 'No product'
		else:		
			count_product = product.quantity - int(qty)
			if int(count_product) < 0:
				if setting.add_cart_product_count_0:
					pass
				else:	
					return "No limit"

		cart_item.qty = int(qty)
		cart_item.item_total = int(qty) * int(cart_item.price)
		cart_item.save()
		new_cart_total = 0
		a_qty = []
		for item in cart.items.all():
			new_cart_total += int(item.item_total)
			a_qty.append(item.qty)
		cart.all_qty = sum(a_qty)	
		cart.cart_total = new_cart_total
		cart.save()	
