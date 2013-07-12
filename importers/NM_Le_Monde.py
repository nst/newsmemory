#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import htmlentitydefs
from urllib import *
from re import *
from myhtmlutils import *
from NM_Interface import *
from sys import *

class NM_Le_Monde(NM_Module):
    """
    Module pour Le Monde
    """

    def urls(self):
        
        base = "http://www.lemonde.fr/web/imprimer_element/0,40-0@2-"
        
        URL = "http://www.lemonde.fr/"
               
        page = urlopen(URL).read()
        
        regexp = compile("/web/article/0,1-0@2-(\d\d\d\d),..-(\d\d\d\d\d\d)")
        f = findall(regexp, page)
        
        l = []
        
        for u in f:
            l.append(base + u[0] + ",50-" + u[1] + ",0.html")
        
        return l
        
    def strip_date(self, page):
        regexp = compile(".*?((LEMONDE\.FR)|(LEMONDE\.FR avec AFP)|(LEMONDE\.FR avec Reuters)|(LEMONDE\.FR avec AFP et Reuters)|(LEMONDE\.FR avec AFP et AP)|(LE MONDE)|(LE MONDE DES LIVRES)) \| (?P<day>\d\d)\.(?P<month>\d\d)\.(?P<syear>\d\d) \| (?P<hour>\d\d)h(?P<minutes>\d\d).*")
        
        #f = findall(regexp, page)
        #print f
        
        m = regexp.search(page)
        """
        print m.group("syear")
        print m.group("month")
        print m.group("day")
        print m.group("hour")
        print m.group("minutes")
        """
        
        #print self.url
        
        return "20" + m.group("syear") + m.group("month") + m.group("day") + m.group("hour") + m.group("minutes") + "00"
        

    def strip_authors(self, page):
        try:
            regexp = compile("<div class=desc><b>(.*?)</b></div>")
            f = findall(regexp, page)[0]
        except:
            f = ""
        
        return f

    def strip_place(self, page):
        #de notre env    

        try:
            regexp = compile(".*?<div class=desc>(.*?)</div>")
            f = findall(regexp, page)[0]
            
            pos = f.find("de notre")
            if pos == -1:
                raise Exception
            
            s = f[:pos-1]
            
            if s.endswith(','):
                return s[:-1]
            else:
                return s
            
        except:
            f = ""
        
        return f

    

    def strip_category(self, page):
        """
        regexp = compile("<span class=tit0>(.*?)</span>")
        try:
            f = findall(regexp, page)[0]
        except:
            f = "" 
               
        return f
        """
        regexp = compile("OAS_sitepage = '(.*?)-LEMONDE")
        try:
            f = findall(regexp, page)[0]
        except:
            f = "" 
        
        #if f == "INTERNATIONAL":
        #    f = "Monde"
        if f == "BUSINESS":
            f = "Entreprise"
        
        return f

    def strip_title_up(self, page):
        regexp = compile("<div class=type-gr>(.*?)</div>")
        f = findall(regexp, page)[0]
        
        return f
    
    def strip_title(self, page):
        regexp = compile("<div class=ar-tit>(.*?)</div>")
        f = findall(regexp, page)[0]
        
        return f
    
    def strip_edition(self, page):
        regexp = compile("<div class=dt>(.*?)</div>")
        try:
            f = findall(regexp, page)[0]
        except:
            f = ""
                
        return f        
    
    def strip_title_down(self, page):
        return ""
    
    def strip_text(self, page):
        regexp = compile(".*<img src.*?let/(..?)\.gif.*?>.*")
        #regexp = compile("img/let/(.)\.gif")
        lettrine = findall(regexp, page)[0]
        
        if len(lettrine) == 2 and lettrine[0] == 'q':
            lettrine = '"' + lettrine[1].upper()
        else:
            lettrine = lettrine.upper()
        
        regexp = compile("<div class=ar-txt>(.*?)</div>", DOTALL)
        f = findall(regexp, page)
        
        length = len(f)
        
        s = lettrine + f[0]
        
        if length > 1:
            for i in range(1, length):
                #s += "\n\n----------\n\n"
                s += f[i]

        #f = findall(regexp, page)[0]
        
        #s = s.replace("<b>", "$£")
        #s = s.replace("</b>", "£$")
        s = s.replace("<br>", "\n")        
        s = s.replace("</p> <p>", "\n")
        s = s.replace("</p><p>", "\n\n")
        s = s.replace("\n\n\n", "\n")
        s = s.replace("<hr>", "\n\n---------------\n\n")
        
        s = remove_tags(s)

        s = s.replace("OAS_AD('Middle1');", "")
        
        #s = s.replace("$£", "<b>")
        #s = s.replace("£$", "</b>")
        
        s = s.lstrip('\n')        
        
        return s

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

        self.source = "Le Monde"
        
        self.url = url

        self.category = self.strip_category(page)
        #print "* ", self.category
        
        self.titleUp   = self.strip_title_up(page)
        #print "* ", self.titleUp
        
        if self.category == '' and self.titleUp != '':
            self.category = self.titleUp
            self.titleUp = ""
            
        self.title     = self.strip_title(page)
        #print "* ", self.title
        
        self.titleDown = self.strip_title_down(page)
        #print "* ", self.titleDown

        self.text  = self.strip_text(page)
        
        if self.strip_edition(page):
            self.text += "\n\n"
            self.text += self.strip_edition(page)
        #print self.text
        
        self.authors = self.strip_authors(page)
        
        self.ts = self.strip_date(page)
        
        self.place = self.strip_place(page)
        
        
        r = {"title":self.title, \
             "titleUp":self.titleUp, \
             "titleDown":self.titleDown, \
             "place":self.place, \
             "source":self.source, \
             "time":self.ts, \
             "link":self.url, \
             "text":self.text, \
             "category":self.category,
             "authors":self.authors}
        
        return r;
    
    def __init__(self):
        pass

if __name__ == "__main__":

    module = NM_Le_Monde()
    
    #urls = module.urls()

    #for u in urls:
    #    print u
    
    urls = ["http://www.lemonde.fr/web/imprimer_element/0,40-0@2-3246,50-853828,0.html"]
    #urls = ['http://www.lemonde.fr/web/imprimer_element/0,40-0@2-3234,50-682516,0.html']
    #urls = ['http://www.lemonde.fr/web/imprimer_element/0,40-0@2-3260,50-682664,0.html']
    
    #urls = ['http://www.lemonde.fr/web/imprimer_element/0,40-0@2-3260,50-682664,0.html']

    #urls = ['http://www.lemonde.fr/web/imprimer_element/0,40-0@2-3218,50-683001,0.html']
    
    for url in urls:
        record = module.record(url)
        for k in record:
            print k, " --> " + record[k]
    
    """
    try:
        record = module.record(url)
        print record
    except:
        print "Exception: ", url
    """




