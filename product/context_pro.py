from  books.models import Cart	



def my_cart(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
		
	except:
		cart = None
	context = {'cart':cart}
	return context	