#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# YAHOO

import htmlentitydefs
from urllib import *
from re import *
from myhtmlutils import *
from NM_Interface import *
import datetime

class NM_Yahoo(NM_Module):
    """
    Module pour les principales rubriques de Yahoo! Actualités
    http://fr.news.yahoo.com/2/
    """
    
    def date_to_timestamp(self, date):
        try:
            date = date.split(' ')
            date = filter(lambda x: x != '', date)
            #print date
    
            day = date[1]
            year = "2007" #date[3][:4]
            #print day
            
            months = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', \
                      'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'décembre']
            month = str(months.index(date[2].strip(',')) + 1)
                
            if(len(day) == 1):
                day = "0" + day
        
            if(len(month) == 1):
                month = "0" + month
            
            (hours, minutes) = date[3].split('h')
            
            if(len(hours) == 1):
                hours = "0" + hours
            
            seconds = "00"
            
            return year + str(month) + day + hours + minutes + seconds
        except:
            return "%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    def strip_title(self, page):
        regexp = re.compile(".*<title>(.*)</title>.*")
        f = findall(regexp, page)[0]
        
        to_remove_from_right = " - Yahoo! Actualit&eacute;s"
        if f.endswith(to_remove_from_right):
            f = f[:-len(to_remove_from_right)]
        
        f = descape(f)
        return f
        
    def strip_block(self, page):
        regexp = compile(".*<cite class=\"auth\">(.*?)</p><script>.*", DOTALL)
        f = findall(regexp, page)[0]
        f = f.strip()
        
        return f#remove_tags(f)
    
    def strip_date(self, page):    
        regexp = compile(".*<span>(.*?)</span>*", DOTALL)
        f = findall(regexp, page)[0]
        return f
    
    def strip_place(self, block):
        regexp = compile(".*<p class=\"first\">(.*?) - *", DOTALL)
        f = findall(regexp, block)

        if f:
            l = f[0].split('\n')
            return l[-1:][0].strip().rstrip(" (AFP)").rstrip(" (AP)").rstrip(" (Reuters)")
        else:
            return ""
            
    def strip_source(self, url):
    
        d = {}
        d['ap'] = "AP"
        d['afp'] = "AFP"    
        d['rtrs'] = "Reuters"    
        
        regexp = compile("http://fr.news.yahoo.com/(.*?)/.*")
        
        source = findall(regexp, url)[0]

        if source in d:
            return d[source]
        else:
            print "source %s unknown" % source
            return None
    
    def strip_text(self, block):
        regexp = compile(".*<p class=\"first\">.*? - (.*)", DOTALL)
        f = findall(regexp, block)[0]
        f = f.replace("</p><p>", "\n\n")
        f = f.replace("<div>", "\n")
        f = f.replace("</div>", "\n")
        f = f.replace("&quot;", '"')
        return remove_tags(f)

    block  = ""

    title  = ""
    place  = ""
    text   = ""
    source = ""
    ts     = ""
    url    = ""
    
    subject = ""
    
    def record(self, url):
        """
        construit un record à partir d'un url
        """
        page = urlopen(url).read()
        #page = open("/Users/nst/Desktop/4i7zh.html").read()

        self.source = self.strip_source(url)
        #print self.source
        
        self.url = url
        #print self.source
        
        self.title = self.strip_title(page)
        #print self.title
        
        self.block = self.strip_block(page)
        #print self.block
        
        self.place = self.strip_place(self.block)
        #print self.place
        
        self.text  = self.strip_text(self.block)
        #print self.text
        
        #print "-->", self.url
        date = self.strip_date(self.block)
        #print "-->", date
        
        self.ts    = self.date_to_timestamp(date)
        
        r = {"title":self.title, \
             "titleUp":'', \
             "titleDown":'', \
             "place":self.place, \
             "source":self.source, \
             "time":self.ts, \
             "link":self.url, \
             "text":self.text, \
             "category":self.cat,
             "authors":""}
        
        return r;
        
    def __init__(self, cat):
        self.cat = cat # "monde", "france", "people", "medias", "insolite", "sante"

    def urls(self):        
        feed = {}
        feed["monde"] = "http://fr.news.yahoo.com/rss/monde.xml"
        feed["france"] = "http://fr.news.yahoo.com/rss/france.xml"    
        feed["economie"] = "http://fr.news.yahoo.com/rss/economie.xml"
        feed["people"] = "http://fr.news.yahoo.com/rss/people.xml"
        feed["insolite"] = "http://fr.news.yahoo.com/rss/insolite.xml"
        feed["sante"] = "http://fr.news.yahoo.com/rss/sante.xml"
        
        page = urlopen(feed[self.cat]).read()
        
        regexp = compile("<link>(.*?)</link>")
        
        #<link>http://fr.news.yahoo.com/afp/20070704/tod-espace-musique-iss-esa-norvege-insol-7f81b96.html</link>
        
        f = findall(regexp, page)
        #print f
        f = map(lambda x:x+"?printer=1", f)
                
        return f



if __name__ == "__main__":

    
    #module = NM_Yahoo("monde")
    module = NM_Yahoo("monde")
    for u in module.urls():
        print u
        try:
            print module.record(u)
        except:
            pass
    
    #adresse = "http://fr.news.yahoo.com/02122005/290/demission-du-ministre-de-l-environnement-chinois.html"
    #adresse = "http://fr.news.yahoo.com/ap/20070704/tfr-social-assurance-maladie-fo-56633fe.html?printer=1"
    #print module.record(adresse)
    #print module.urls()
    import sys
    sys.exit(0)
    """
    module = NM_Yahoo("france") 
    adresse = "http://fr.news.yahoo.com/afp/20070708/tfr-auto-gouvernement-sport-a8f5b30.html?printer=1"
    print module.record(adresse)
    
    import sys
    sys.exit(0)
    """
    #try:
    #    adresse = "http://fr.news.yahoo.com/21022007/202/pres-de-700-kg-de-fromage-voles-dans-une-fromagerie.html"
    #    print module.record(adresse)
    #except:
    #    print "Exception: ", adresse
    
    
    
    urls = module.urls()
    #print urls
    
    for url in urls:
        print url
        try:
            record = module.record(url)
            print record
        except:
            print "Exception: ", url
    
