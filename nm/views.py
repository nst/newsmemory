from django.db import models, backend
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
#from django import forms
from django import oldforms as forms
from django.core import template_loader
from django.conf import settings
from django.template import RequestContext

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.views.generic.list_detail import object_list, object_detail
#from django.views.generic.create_update import create_object, update_object, delete_object

from newsmemory.nm.models import *
import datetime

# Create your views here.

class QueryManipulator(forms.Manipulator):

    def __init__(self):        
        self.fields = (
            forms.TextField(field_name="q", is_required=True),
        )
    
    def execute_query(self, q):
        print "-", q
        d = {}
        d['newsitems'] = Newsitem.objects.search(q['q']).order_by('-time')
        return d

def newsitem(request, object_id):
    d = {}
    d['user'] = request.user

    newsitem = Newsitem.objects.get(pk=object_id)
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect(newsitem.link)
        
    log = Log(user=request.user, newsitem=newsitem)
    try:
        log.save()
    except:
        pass
    
    log = Log.objects.filter(user=request.user, newsitem=newsitem)[0]
    d['is_flagged'] = log.marked
    
    d['object'] = newsitem
    if 'q' in request.session:
        d['q'] = request.session['q']
    return render_to_response('nm/newsitem_detail.html', d, context_instance=RequestContext(request))
#newsitem = login_required(newsitem)

def set_flag(request, object_id, value):
    newsitem = Newsitem.objects.get(pk=object_id)
    
    log = Log.objects.filter(user=request.user, newsitem=newsitem)[0]
    log.marked = value
    log.save()

    return HttpResponseRedirect("/newsitems/%d" % newsitem.id)    
    
    #d['object'] = newsitem
    #return render_to_response('nm/newsitem_detail.html', d)  

def flag(request, object_id):
    return set_flag(request, object_id, True)    
flag = login_required(flag)

def unflag(request, object_id):
    return set_flag(request, object_id, False)    
unflag = login_required(unflag)


"""
def limited_object_list(*args, **kwargs):
    return object_list(*args, **kwargs)
limited_object_list = login_required(limited_object_list)

def limited_object_detail(*args, **kwargs):
    return object_detail(*args, **kwargs)
limited_object_detail = login_required(limited_object_detail)
"""

def news_by_day(request):
    d = {}
    d['user'] = request.user
    d['news_by_day'] = True
    
    manipulator = QueryManipulator()
    
    date = datetime.datetime.now().date()
    date_next = date + datetime.timedelta(1)
    
    if request.method == 'GET':    
        try:
            date_tuple = request.GET['date'].split('-')
            date_tuple = map(int, date_tuple)
            
            date = datetime.date(date_tuple[0], date_tuple[1], date_tuple[2])
            date_next = date + datetime.timedelta(1)
            d['date_next'] = date_next
            
        except:
            pass
    
    d['date'] = date
    
    date_previous = date + datetime.timedelta(-1)
    
    d['date_previous'] = date_previous
    
    qs = Newsitem.objects.select_related().filter(time__range=(date, date_next)).filter(Q(source__name="AFP") | Q(source__name="AP") | Q(source__name="Reuters") | Q(source__name="ATS")).order_by('-time')
    
    return object_list(request, qs, paginate_by=1000, template_name="nm/news_by_day.html", extra_context = d)

#news_by_day = login_required(news_by_day)

def news_by_source(request, **kwargs):
    import datetime
    
    d = {}
    d['user'] = request.user
    d['source_url'] = kwargs['source_url']
    d['source'] = Source.objects.filter(name=kwargs['source'])[0]

    date = datetime.datetime.now().date()
    date_previous = date + datetime.timedelta(-30)
    
    qs = Newsitem.objects.select_related().filter(time__range=(date_previous, date)).filter(source__name=kwargs['source']).order_by('-time')

    return object_list(request, qs, paginate_by=1000, template_name="nm/news_by_source.html", extra_context=d)
    
#news_by_source = login_required(news_by_source)

def flagged_news(request, **kwargs):
    
    d = {}
    d['user'] = request.user

    queryset = Newsitem.objects.select_related().filter(log__marked=True).order_by('-time')
    
    return object_list(request, queryset, paginate_by=100, template_name="nm/flagged_news.html", extra_context = d)
    
#flagged_news = login_required(flagged_news)

def search(request):
    items_per_page = 30
    
    d = {}
    d['user'] = request.user

    manipulator = QueryManipulator()
    
    if request.method == 'POST':
        new_data = request.POST.copy()

        errors = manipulator.get_validation_errors(new_data)

        if not errors:
            manipulator.do_html2python(new_data)
            result = manipulator.execute_query(new_data)

            request.session['results'] = result['newsitems']
            
            d['q'] = new_data['q']
            request.session['q'] = new_data['q']

            # Create the FormWrapper, template, context, response.
            form = forms.FormWrapper(manipulator, new_data, errors)
            d['form'] = form

            queryset = request.session['results']
            return object_list(request, queryset, paginate_by=items_per_page, template_name="nm/search.html", extra_context = d)
            
    else: # 'GET'
        errors = new_data = {} # No POST, so we want a brand new form without any data or errors.
        
        if 'page' not in request.GET:
            request.session['results'] = None
            request.session['q'] = ""

    # Create the FormWrapper, template, context, response.
    form = forms.FormWrapper(manipulator, {'q':request.session['q']}, errors)
    d['form'] = form

    if 'results' in request.session and request.session['results'] != None:
        d['q'] = request.session['q']
        queryset = request.session['results']
        return object_list(request, queryset, paginate_by=items_per_page, template_name="nm/search.html", extra_context = d)
    
    queryset = Newsitem.objects.filter(pk=0)
    return object_list(request, queryset, paginate_by=1, template_name="nm/search.html", extra_context = d)

search = login_required(search)
