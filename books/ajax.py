from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from .models import *
from django.contrib.auth  import get_user_model
User = get_user_model()
import json

def search_login(request):
	login = request.GET.get('q')
	data = {}
	try:
		email = User.objects.get(username=login)
		data['email'] = 'ok'
	except:
		data['email'] = 'error'
			
	emails = User.objects.filter(username=login).count()
	if int(emails) > 0:
		data['status'] = 'error'
	else:	 	
		data['status'] = 'ok'
	return JsonResponse(data)

def search_subcategory(request):
	category_id = request.GET.get('q')
	data = {}
	try:
		category = Category.objects.get(id=category_id)
		subcategories = category.subcategory_set.all()
		if subcategories.count() > 0:
			data['status'] = 'ok'
			grop = []
			for s in subcategories:
				gr = []
				gr.append(s.id)
				gr.append(s.title)
				grop.append(gr)
			data['subcategories'] = grop	
		else:
			data['subcategories'] = []	
			data['status'] = 'no-match'
	except:		
			data['status'] = 'error'
	return JsonResponse(data)		
				

def download_providers(request):
	providers = Provider.objects.all()
	data = {}
	grop = []
	if providers.count() > 0:
		for s in providers:
			gr = []
			gr.append(s.id)
			gr.append(s.name)
			grop.append(gr)
		data['status'] = 'ok'
		data['providers'] = grop
	else:	
		data['status'] = 'no-result'
		data['providers'] = []
	return JsonResponse(data)	

def add_provider(request):
	d = request.GET.get('q')
	data = json.loads(d)
	name = data['name']
	phone = data['phone']
	adress = data['adress']
	data = {}
	# try:
	m = Provider.objects.create(name=name,phone=phone,adres=adress)
	data['status'] = 'ok'
	# except:	
	# 	data['status'] = 'error'
	return JsonResponse(data)	
