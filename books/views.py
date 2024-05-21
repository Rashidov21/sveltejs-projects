from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .models import *
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib import messages
import datetime
from django.core.paginator import Paginator
from product.ajax import generator_month
from product.helper import paginate_generator
today = datetime.date.today()
tod = datetime.datetime.now()
cur_month = tod.strftime('%B')
month = generator_month(cur_month)
from io import BytesIO
from django.conf import settings
from django.template.loader import render_to_string
# import weasyprint
import os
from django.core.files import File

from django.http import JsonResponse
# Create your views here.

def index(request):
	return render(request, 'index.html')

# Page Viewer method
def page_views(request, page_name):
	return render(request, 'pages/{}.html'.format(page_name))

def login_view(request):
	return render(request, 'pages/login.html')




class AddProduct(View):
	def get(self, request):
		
		categories = Category.objects.all()
		providers = Provider.objects.all()
		last_products = Product.objects.filter(check=False)
		product_count = last_products.count()
		paginator = paginate_generator(request,last_products)
		context = {'categories':categories,'providers':providers,'is_paginated':paginator['is_paginated'],'next_url':paginator['next_url'],'prev_url':paginator['prev_url']}
		context['page_object'] = paginator['page_object']
		context['product_count'] = product_count
		return render(request, 'product/add.html',context)

	def post(self, request):
		
		title = request.POST['title']
		category_id = request.POST['category']
		category = Category.objects.get(id=category_id)
		quantity = request.POST['quantity']
		pur_price = request.POST['pur_price']
		cur_price = request.POST['cur_price']
		try:
			provider_id = request.POST['provider']
			provider = Provider.objects.get(id=provider_id)
		except:	
			provider = None
		try:
			subcategory_id = request.POST['subcategory']
			subcategory = SubCategory.objects.get(id=provider_id)
		except:	
			subcategory = None	


		fields = ['author','edition','info']
		create_fields = {}
		for f in fields:
			try:	
				request.POST[f]
				create_fields[f] = request.POST[f]
			except:	
				create_fields[f] = None
				
		p = Product.objects.create(category=category,month=month,subcategory=subcategory,
			title=title,author=create_fields['author'],edition=create_fields['edition'],
			provider=provider,date=today,description=create_fields['info'],quantity=quantity,
			pur_price=pur_price,cur_price=cur_price)
		
		messages.add_message(request,messages.SUCCESS,"Tovar qo'shildi")
		return HttpResponseRedirect(reverse('books:add'))									

def edit_info_product(request):
	if request.method == "POST":
		try:
			subcategory_id = request.POST['subcategory']
			subcategory = SubCategory.objects.get(id=provider_id)
		except:	
			subcategory = None
		category_id = request.POST['category']
		product_id = request.POST['product_id']
		
		product = Product.objects.get(id=product_id)
		category = Category.objects.get(id=category_id)
		fields = ['title','quantity','edition','author','pur_price','cur_price','info']
		create_fields = {}
		for f in fields:
			try:	
				info = request.POST[f]
				create_fields[f] = request.POST[f]
			except:	
				create_fields[f] = None

		product.category = category		
		product.subcategory = subcategory		
		product.title = create_fields['title']		
		product.quantity = create_fields['quantity']		
		product.edition = create_fields['edition']		
		product.author = create_fields['author']		
		product.pur_price = create_fields['pur_price']		
		product.cur_price = create_fields['cur_price']		
		product.info = create_fields['info']
		product.save()
		messages.add_message(request,messages.SUCCESS,"Tovar xaqidagi ma'lumotlar o'zgartirildi")
		return HttpResponseRedirect(reverse('books:add'))

class Delivery(View):
	def get(self, request):
		delivery = AddProductArchive.objects.all()[:50]
		paginator = paginate_generator(request,delivery)
		context = {'is_paginated':paginator['is_paginated'],'next_url':paginator['next_url'],'prev_url':paginator['prev_url']}											
		context['page_object'] = paginator['page_object']
		return render(request,'pages/delivery-list.html',context)

def delivery_products(request,delivery_id):
	print(os.getcwd())	
	delivery = AddProductArchive.objects.get(id=delivery_id)
	products = delivery.product.all()
	paginator = paginate_generator(request,products)
	context = {'is_paginated':paginator['is_paginated'],'next_url':paginator['next_url'],'prev_url':paginator['prev_url']}											
	context['page_object'] = paginator['page_object']
	context['delivery'] = delivery
	return render(request,'pages/delivery-product-list.html',context)



def admin_order_pdf(request,bot=None):
	print("Working admin_order_pdf")
	delivery_id = request.GET.get('value')	
	delivery = AddProductArchive.objects.get(id=delivery_id)
	products = delivery.product.all()
	context = {}											
	context['page_object'] = products
	context['delivery'] = delivery
	data = {}
	
	html = render_to_string('to_print/tovar_kirim.html', context)
	out = BytesIO()
	stylesheets=[weasyprint.CSS(settings.STATIC_ROOT +'/dist/css/bootstrap.min.css')]
	# weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
	path = os.path.abspath('/home/ibroxim/Документы')
	formate = 'pdf'
	name = "{0}_{1}_{2}_{3}.{4}".format(delivery.provider.name,delivery.day,delivery.month,delivery.year,formate)
	FileFullPath = os.path.join(path, name)
	
	with open(FileFullPath, 'wb') as new_file:
		new_file.write(out.getvalue())
	delivery.save_as_folder = True	
	delivery.save()	
	if not delivery.pdf:
		file = open(FileFullPath,'rb')
		delivery.pdf.save(file.name, File(file))
		delivery.save()	
	# response = HttpResponse(content_type='application/pdf')
	
	# response['Content-Disposition'] = 'filename=\
	# "tovar_kirim.pdf"'
	
	# weasyprint.HTML(string=html).write_pdf(response,
	# stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/dist/css/bootstrap.min.css')])
	data['status'] = 'ok'
	if bot:
		return data
	else:	
		return JsonResponse(data)

def print_me(request, delivery_id):
	delivery = AddProductArchive.objects.get(id=delivery_id)
	products = delivery.product.all()
	paginator = paginate_generator(request,products)
	context = {}											
	context['page_object'] = products
	context['delivery'] = delivery
	context['print'] = True
	return render(request, 'to_print/tovar_kirim.html', context)

