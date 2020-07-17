from django.core.paginator import Paginator
import re
from django.db.models import Q

def paginate_generator(request,obj_list):
	try:
		paginator = Paginator(obj_list, 30)

	except:
		result = "error"	
	page_number = request.GET.get('page',1)
	page = paginator.get_page(page_number)
	is_paginated = page.has_other_pages()
	
	if page.has_previous():
		prev_url = '?page={}'.format(page.previous_page_number())
	else:
		prev_url = ''
	
	if page.has_next():
		next_url = '?page={}'.format( page.next_page_number())
	else:
		next_url = ''
	result = {'page_object':page,'is_paginated':is_paginated,'next_url':next_url,'prev_url':prev_url}
	return result	


def normalize_query(query_string,
    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
    normspace=re.compile(r'\s{2,}').sub):


    res = [normspace(' ',(t[0] or t[1]).strip()) for t in findterms(query_string)]	
 

    return res

def get_query(query_string, search_fields):

    '''
    Returns a query, that is a combination of Q objects. 
    That combination aims to search keywords within a model by testing the given search fields.
    '''

    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query    

  