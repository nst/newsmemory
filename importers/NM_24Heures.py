#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import thread
import htmlentitydefs
from urllib import *
from re import *
from myhtmlutils import *
from NM_Interface import *
from sets import *

def is_white_line(line):
    line = line.replace(' ', '')
    return len(line) == 0

class NM_24Heures(NM_Module):
    
    def strip_date(self, page):
        regexp = compile("</ul>    	<p>(.*?)\|(.*?)\|(.*?)</p>")
        (author, date, time) = findall(regexp, page)[0]
                
        date = date.strip()
        time = time.strip()
        if len(time) > 5:
            time = time[:5]

        (day, month, year) = date.split(' ')
        (h, m) = time.split('h')

        months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', \
                  'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
        month = str(months.index(month) + 1)
    
        if(len(month) == 1):
            month = "0" + month
        
        return year + month + day + h + m + "00"

    def strip_title_up(self, page):
        regexp = compile("<title>(.*?)</title>")
        f = findall(regexp, page)[0]
        print f
        f = f[len("24 Heures - Detail Vaud - "):]
        print f
        parts = f.split(' - ')
        print parts
        if len(parts) > 1:
            parts = parts[0:1]
        return parts[0]

    def strip_title(self, page):
        regexp = compile("<title>(.*?)</title>")
        f = findall(regexp, page)[0]

        f = f.lstrip("24 Heures - Detail Vaud -")
        f = f.strip()
        
        dash_index = f.find(' - ')
        if dash_index != -1:
            f = f[dash_index+3:].strip()
        
        return f

    def strip_authors(self, page):
        regexp = compile("</ul>    	<p>(.*?)\|(.*?)\|(.*?)</p>")
        (author, date, time) = findall(regexp, page)[0]
        return author

    def strip_text(self, page):
        regexp = compile("<div id=\"zone_article_txt\" class=\"petit\">(.*?)<div class=\"clear\"></div>", DOTALL)
        f = findall(regexp, page)
        
        f = "".join(f[0])
        
        f = f.replace("</p><p>", "\n\n")
        
        f = remove_tags(f)

        f = f.strip()            
        
        return f

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
        
        if url.startswith('http://24heures.ch/pages/home/24_heures/l_actu/vaud/'):
            self.category = 'Vaud'
        else:
            raise ValueError
        
        self.source = "24Heures"
        
        self.url = url
        
        page = urlopen(url).read()
        page = page.replace('\222', "'")

        self.titleUp = self.strip_title_up(page)
                
        self.title = self.strip_title(page)
        
        self.titleDown = ""

        self.authors = self.strip_authors(page)

        self.text = self.strip_text(page)
        
        self.ts = self.strip_date(page)
        
        r = {"title":self.title,
             "titleUp":self.titleUp,
             "titleDown":self.titleDown,
             "place":self.place,
             "source":self.source,
             "time":self.ts,
             "link":self.url,
             "text":self.text,
             "category":self.category,
             "authors":self.authors}
        
        return r
    
    def __init__(self):
        pass
        
    def urls(self):
        URL = "http://24heures.ch/pages/home/24_heures/l_actu/vaud/"
        
        page = urlopen(URL).read()
                
        set = Set()
        
        regexp = compile("/pages/home/24_heures/l_actu/vaud/detail_vaud/\(contenu\)/\d*")
        
        f = findall(regexp, page)
        
        if f:
            for url_end in f:
                set.add("http://24heures.ch" + url_end)
        
        return list(set)

if __name__ == "__main__":

    module = NM_24Heures()

    for u in module.urls():
        print u

    #urls = ['http://24heures.ch/pages/home/24_heures/l_actu/vaud/detail_vaud/(contenu)/54079']

    #urls = module.urls()
    
    for url in urls:
        #print url
        try:
            record = module.record(url)
            for f in record:
                print f, " ---> ", record[f]
        except:
            pass



