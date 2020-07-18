from django import template
register = template.Library()


@register.filter(name='product_summa')
def product_summa(price,qty):
	res = int(price) * int(qty)
	return res

	