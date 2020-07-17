from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from books.models import *
from .models import *
from .forms import *
from .ajax import *
from .helper import *
from django.contrib import messages
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
today = datetime.date.today()
tod = datetime.datetime.now()
cur_month = tod.strftime('%B')
month = generator_month(cur_month)
year = today.year
day = today.day
# Create your views here.


class ArchiveAddProduct(View):
	def get(self ,request):
		print('Workin get')
		setting = Settings.objects.latest('-id')
		limit = int(setting.page_product_limit)
		products = Product.objects.all()[:limit]
		paginator = paginate_generator(request,products)
		categories = Category.objects.all()
		context = {'categories':categories,'setting':setting,
					'day':day,'month':month,'year':year,
					'is_paginated':paginator['is_paginated'],'next_url':paginator['next_url'],
					'prev_url':paginator['prev_url']}
		context['get'] = True
		context['page_object'] = paginator['page_object']
		return render(request, 'product/archive.html',context)

	def post(self, request):
		setting = Settings.objects.latest('-id')
		print('Workin post')
		today = datetime.date.today()
		tod = datetime.datetime.now()
		cur_month = tod.strftime('%B')
		month = generator_month(cur_month)
		year = today.year
		day = today.day
		categories = Category.objects.all()
		try:
			c_id = request.POST['select_category']
			category = Category.objects.get(id=c_id)
			products = category.product_set.all()
			paginator = paginate_generator(request,products)
			context = {'day':day,'setting':setting,'month':month,'categories':categories,'year':year,
					'is_paginated':paginator['is_paginated'],'next_url':paginator['next_url'],
					'prev_url':paginator['prev_url'],'page_object':paginator['page_object']}
			return render(request, 'product/archive.html',context)
		except:
			c_id = None
		try:			
			date = request.POST['date']
			number_month = date.split('-')[1]
			day = date.split('-')[2]
			year = date.split('-')[0]
			month = name_month(number_month)
			print(day)
			products = Product.objects.filter(date=date)
			paginator = paginate_generator(request,products)
			context = {'day':day,'setting':setting,'month':month,'categories':categories,'year':year,
					'is_paginated':paginator['is_paginated'],'next_url':paginator['next_url'],
					'prev_url':paginator['prev_url'],'page_object':paginator['page_object']}
			return render(request, 'product/archive.html',context)
		except:
			return HttpResponseRedirect(reverse('product:archive_product'))

def catalog_view(request,catalog_id):
	try:
		setting = Settings.objects.latest('-id')
		category = Category.objects.get(id=catalog_id)
		products = category.product_set.all()
		paginator = paginate_generator(request,products)
		context = {'is_paginated':paginator['is_paginated'],'next_url':paginator['next_url'],
					'prev_url':paginator['prev_url'],'setting':setting,'page_object':paginator['page_object']}
		return render(request, 'pages/category.html',context)
	except:
		return render(request,'pages/404.html')	

def dynamic_catalog(request):
	print('dynamic_catalog post')
	today = datetime.date.today()
	tod = datetime.datetime.now()
	cur_month = tod.strftime('%B')
	month = generator_month(cur_month)
	year = today.year
	day = today.day
	categories = Category.objects.all()
	try:
		c_id = request.POST['select_category']
		category = Category.objects.get(id=c_id)
		products = category.product_set.all()
		paginator = paginate_generator(request,products)
		context = {'day':day,'month':month,'categories':categories,'year':year,
				'is_paginated':paginator['is_paginated'],'next_url':paginator['next_url'],
				'prev_url':paginator['prev_url'],'page_object':paginator['page_object']}
		return render(request, 'product/archive.html',context)
	except:
		return render(request,'pages/404.html')	




def cart_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	print(cart)		
	context = {
	'cart':cart,'close_wrapper_cart':True
	}
	return render(request, 'pages/cart.html', context)

def invoice(request):
	clients = Client.objects.all()
	paginator = paginate_generator(request,clients)
	context = {'is_paginated':paginator['is_paginated'],'next_url':paginator['next_url'],
					'prev_url':paginator['prev_url']}
	context['page_object'] = paginator['page_object']
	return render(request, 'pages/invoice.html', context)

def toprint(request,client_id):
	try:
		client = Client.objects.get(id=client_id)
	except:
		messages.add_message(request,messages.WARNING, "Mijoz topilmadi!")
		return HttpResponseRedirect(reverse('product:invoice'))
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		messages.add_message(request,messages.WARNING, "Savatcha topilmadi!")
		return HttpResponseRedirect(reverse('product:invoice'))
	context = {'client':client,'cart':cart}
	return render(request ,'pages/toprint.html',context)
