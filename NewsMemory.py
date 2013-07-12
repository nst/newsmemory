#!/usr/bin/python
# -*- coding: utf-8 -*-

#from imp import *
import importers
#import sys
from datetime import *
from importers import BadSourceException

"""
def import_importer(name):
    #from importers.name import * 
    print name
    __import__("importers.%s" % name, locals(), globals(), [''])
    #importer.find_module(name, path=None)
"""
    
    
import os

try:
    my_importers = os.listdir('/Users/macmini/newsmemory/importers/')
except:
    my_importers = os.listdir('/Users/nst/Projects/newsmemory/importers/')

my_importers = filter(lambda x:x.startswith('NM_') and x.endswith('.py'), my_importers)
my_importers = map(lambda x:x[:-3], my_importers)
my_importers = map(lambda x:"importers." + x, my_importers)

map(__import__, my_importers)


#from DB import *
#from importers.NM_Yahoo import *
#from importers.NM_Swissinfo import *
#from importers.NM_Edicom import *
#from importers.NM_ISN import *
#from importers.NM_Le_Monde import *
#from importers.NM_24Heures import *
import time

os.environ['DJANGO_SETTINGS_MODULE'] = "settings"
from nm.models import *

#print os.environ


def repair_encoding(s):
    try:
        return s.decode('latin-1').encode('utf-8')
    except:
        return s

def url_in_db(url):    
    try:
        result = Newsitem.objects.get(link=url)
        return True
    except AssertionError:
        return True # multiple !
    except:
        return False

def add_news(news):
    news["source"] = repair_encoding(news["source"])
    try:
        source = Source.objects.get(name=news["source"])
    except:
        source = Source()
        source.name = news["source"]
        source.save()

    news["place"] = repair_encoding(news["place"])
    try:
        place = Place.objects.get(name=news["place"])
        #print "got place ", place
    except:
        place = Place()
        place.name = news["place"]
        place.save()
        print "added place", place.name

    news["category"] = repair_encoding(news["category"])
    print "category ", news["category"]
    try:
        news["category"] = Category.objects.get(name=news["category"].title())
    except:
        category = Category()
        category.name = news["category"]
        category.save()
        news["category"] = category
    
    newsitem = Newsitem(titleUp = repair_encoding(news['titleUp']),
                        title = repair_encoding(news['title']),
                        titleDown = repair_encoding(news['titleDown']),
                        authors = repair_encoding(news['authors']),
                        text = repair_encoding(news['text']),
                        link = news['link'],
                        time = news['time'],
                        category = repair_encoding(news['category']),
                        source = source,
                        place = place)
    
    newsitem.save()
    
class NewsMemory:
    def __init__(self):
        self.modules = [importers.NM_Yahoo.NM_Yahoo("monde"),
                   importers.NM_Yahoo.NM_Yahoo("france"),
                   importers.NM_Yahoo.NM_Yahoo("people"),
                   importers.NM_Yahoo.NM_Yahoo("economie"),
                   importers.NM_Yahoo.NM_Yahoo("insolite"),
                   importers.NM_Yahoo.NM_Yahoo("sante"),
                   importers.NM_Swissinfo.NM_Swissinfo(),
                   importers.NM_Edicom.NM_Edicom(),
                   importers.NM_ISN.NM_ISN(),
                   importers.NM_Le_Monde.NM_Le_Monde(),
                   importers.NM_24Heures.NM_24Heures()]

    def run_on_modules(self):
        for m in self.modules:        
            urls = m.urls()
            for url in urls:
                if url_in_db(url):
                    print "skip " + url
                    #pass
                else:
                    try:
                        r = m.record(url)
                        if r:
                            add_news(r)
                            print time.ctime() + "     " + url
                    except BadSourceException, e:
                        print e, url
                        #pass
                    except:
                        print datetime.datetime.now(), "xxx", url

    def generate_rss(self):
        from django.conf import settings
        from django.utils import feedgenerator
        from nm.models import Newsitem
        import os
        
        file_name = "latest_news.rss"
        file_path = os.sep.join([settings.MEDIA_ROOT, file_name])
        file_url = os.sep.join([settings.MEDIA_URL, "site_media", file_name])
        
        feed = feedgenerator.Rss201rev2Feed(
            title=u"Newsmemory",
            link=file_url,
            description=u"Dernières nouvelles",
            language=u"fr",
        )
        
        start_date = datetime.datetime.now() - timedelta(days=1)
        
        qs = Newsitem.objects.select_related().filter(time__gt=start_date).filter(Q(source__name="AFP") | Q(source__name="AP") | Q(source__name="Reuters") | Q(source__name="ATS")).order_by('-time')[:50]
        print "qs.count()", qs.count()
        # TODO break lines in text
        # TODO display source and original link
        for r in qs:
            # text = "<br />".join([r.source.name, "%s" % r.time, r.text]) 
            feed.add_item(title=r.title, link=r.get_absolute_url(), description="")
        
        fp = open(file_path, 'w')
        feed.write(fp, 'utf-8')
        fp.close()


if __name__ == "__main__":
    nm = NewsMemory()
    nm.run_on_modules()
    nm.generate_rss()

