from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .models import *
from django.http import HttpResponseRedirect
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

