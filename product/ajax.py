from books.models import *
from .models import *
from .helper import *
from django.http import JsonResponse
import json


def generator_month(month):
    if month == 'January':
        month = 'Yanvar'
    elif month[0] == 'D':
        month = 'Dekabr'
    elif month[0] == 'F':
        month = 'Fevral'
    elif month == 'March':
        month = 'Mart' 
    elif month[0] == 'A':
        month = 'Aprel'
    elif month == 'May':
        month = 'May'
    elif month == 'June':
        month = 'Iyun'
    elif month == 'July':
        month = 'Iyul' 
    elif month[0] == 'A':
        month = 'Avgust'
    elif month[0] == 'S':
        month = 'Sentabr'
    elif month[0] == 'O':
        month = 'Oktabr'
    elif month[0] == 'N':
        month = 'Noyabr'                                 
    return month

def name_month(number):
	number = str(number)
	if number == '01':
		number = 'Yanvar'
	elif  number == '02':
		month = 'Fevral'
	elif number == '03':
		number = 'Mart'
	elif  number == '04':
		number = 'Aprel' 
	elif number  == '05':
		number = 'May'
	elif  number == '06':
		number = 'Iyun'
	elif  number == '07':
		number = 'Iyul'
	elif number == '08':
		number = 'Avgust' 
	elif number == '09':
		number = 'Sentabr'
	elif number  == '10':
		number = 'Oktabr'
	elif number  == '11':
		number = 'Noyabr'
	elif number  == '12':
		number = 'Dekabr'                                 
	return number

def search_date(request):
	date = request.GET.get('date')
	print(date)
	data = {}
	products = Product.objects.filter(date=date)
	if products.count() > 0:
			data['status'] = 'ok'
			grop = []
			for s in products:
				gr = []
				gr.append(s.id)
				gr.append(s.title)
				gr.append(s.category.title)
				gr.append(s.edition)
				gr.append(s.quantity)
				gr.append(s.pur_price)
				gr.append(s.cur_price)
				gr.append(s.date)
				grop.append(gr)
			data['products'] = grop	
	else:
		data['products'] = []	
		data['status'] = 'no-match'
	return JsonResponse(data)

def add_to_cart_view(request):
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
	product_id = request.GET.get('product_id')		
	product = Product.objects.get(id=product_id)
	
	res = cart.add_to_cart(product.id)
	if res == "Added":
		return JsonResponse({'code':400})
	elif res == "No product":
		return JsonResponse({'code':500})
	else:	
		new_cart_total = 0.00
		for item in cart.items.all():
			new_cart_total += int(item.item_total)
		cart.cart_total = new_cart_total
		cart.save()	
		return JsonResponse({'code':200,'cart_total':cart.items.count(), 
			'cart_total_price':cart.cart_total,'product_total':product.quantity})

def change_item_qty(request):
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
	data = {}	
	d = request.GET.get('value')
	d = json.loads(d)	
	qty = d['qty']
	item_id = d['item_id']
	cart_item = CartItem.objects.get(id=int(item_id))
	cart_item.qty = int(qty)
	cart_item.item_total = int(qty) * int(cart_item.product.cur_price)
	cart_item.save()
	try:
		res = cart.change_qty(int(qty), int(item_id))
		if res == 'No product':
			data['status'] = 'no product'
		elif res == 'No limit':
			data['status'] = 'no limit'
		else:	
			data = {'status':'ok','cart_total':cart.items.count(),
		 	'item_total':cart_item.item_total,
		 	'cart_total_price':cart.cart_total,'all_product_count':cart.all_qty,
		 	'product_count':cart_item.product.quantity}

		return JsonResponse(data)
	except:
		return JsonResponse({'status':'error'})	

def control_price(request):
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
	d = request.GET.get('value')
	d = json.loads(d)	
	price = d['price']
	item_id = d['item_id']
	cart_item = CartItem.objects.get(id=int(item_id))
	cart_item.price = int(price)
	cart_item.item_total = int(price) * int(cart_item.qty)
	cart_item.save()
	cart.change_qty(cart_item.qty,int(item_id))	
	data = {
		 'item_total':cart_item.item_total,
		 'cart_total_price':cart.cart_total,'status':'ok'}

	return JsonResponse(data)	 




def remove_from_cart_view(request):
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
	d = request.GET.get('value')
	d = json.loads(d)
	product_id = d['product_id']
	item_id = d['item_id']
	cart_item = CartItem.objects.get(id=int(item_id))		
	product = Product.objects.get(id=product_id)
	cart.remove_from_cart(product.id)
	new_cart_total = 0
	for item in cart.items.all():
		new_cart_total += int(item.item_total)
	cart.cart_total = new_cart_total
	cart.save()
	all_count = []
	for c in cart.items.all():
		all_count.append(int(c.qty))
	all_product_count = sum(all_count)
	data = 	{'cart_total':cart.items.count(), 'item_total':cart_item.item_total,
	 'cart_total_price':cart.cart_total,'all_product_count':all_product_count,
	 'status':'ok'}
	return JsonResponse(data)		 


def loading_cart(request):
	data = {'list':[]}
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
		p = cart.items.all()
		for item in p:
			data['list'].append({'title':item.product.title,'id':item.id,'category':item.product.category.title,
									'cur_price':item.product.cur_price,'quantity':item.product.quantity,
									'qty':item.qty,'product_id':item.product.id,
									'product_total':item.product.quantity,'cart_total':cart.cart_total})
	except:
			cart = None

	return JsonResponse(data)


def reset_cart(request):
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
	data = {}	
	if cart.items.count() == 0:
		data['status'] = 'no product'
	else:
		cart.items.all().delete()
		cart.cart_total = 0
		cart.all_qty = 0
		cart.save()
		data['status'] = 'ok'
		data['cart_total_price'] = cart.cart_total
		data['all_product_count'] = cart.all_qty

	return JsonResponse(data)

def add_client(request):
	d = request.GET.get('value')
	d = json.loads(d)
	name = d['name']
	adres = d['adres']
	contract_number = d['contract_number']
	inn = d['inn']
	reg_code = d['reg_code']
	director = d['director']
	counter = d['counter']
	phone = d['phone']
	c = Client.objects.create(name=name,adres=adres,contract_number=contract_number,
				phone=phone,inn_number=inn,reg_code=reg_code,director=director,counter=counter)
	data = {'result':'ok'}
	return JsonResponse(data)




def search_product(request):
	query_string = ''
	found_entries = None
	data = {'status':None,'list':[]}		
	if ('value' in request.GET) and request.GET['value'].strip():
		print('Working if')		
		query_string = request.GET['value']
		entry_query = get_query(query_string, ['title', 'author', 'edition'])
		found_entries = Product.objects.filter(entry_query).order_by('-id')
		print(found_entries)
		for f in found_entries:
			data['list'].append({'title':f.title,'category':f.category.title,
				'category_id':f.category.id,'price':f.cur_price,
				'quantity':f.quantity,'product_id':f.id})
	else:
		data['status'] = 'error'				
	return JsonResponse(data)
			
	return JsonResponse(data)	
			



