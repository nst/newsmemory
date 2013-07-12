#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# Swissinfo

import htmlentitydefs
from urllib import *
from re import *
from myhtmlutils import *
from NM_Interface import *
from sys import *

class NM_Edicom(NM_Module):
    """
    Module pour la rubrique Suisse de Edicom
    http://www.edicom.ch/news/suisse/
    """
    
    def strip_title(self, page):
        regexp = compile("<span class=\"newsDetailTitre\">(.*?)</span>")
        f = findall(regexp, page)[0]
        f = descape(f)
        return f
    
    def strip_block(self, page):
        regexp = compile("<span style=\"text-align:justify\">(.*?)</h2>", DOTALL)
        f = findall(regexp, page)[0]

        f = descape(f)

        f = f.replace("<BR>", "\n")
        f = f.replace("<br>", "\n")
        f = f.replace("<p>", "\n")
        f = f.replace("</p>", "\n")
        f = f.replace("<h2>", "\n")
        f = f.replace("<BR />", "\n")    
        
        f = f.lstrip("\n")
        f = f.rstrip("\n")
        #print f
        return f
    
    def strip_timestamp(self, page):
        regexp = compile("<div class=\"newsTitleDerniere2\">(.*?)</div>")
        date = findall(regexp, page)[0]
        #print date
        
        regexp = compile("(\d{1,2}) (\S*) (\d{4}) - (\d{2}):(\d{2})")
        #print findall(regexp, date)[0]
        (day, month, year, hour, minute) = findall(regexp, date)[0]
        
        """
        print day
        print month
        print year
        print hour
        print minute
        """
        
        months = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', \
                  'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
        month = str(months.index(month) + 1)
        if(len(month) == 1):
            month = "0" + month

        return year + month + day + hour + minute + "00"

    def strip_source(self):
        ats_string = "© ats. - Tous droits réservés. "
        ap_string = "© ap. - Tous droits réservés. "

        if self.block.endswith(ats_string):
            source = "ATS"
            to_del_r = len(ats_string)
            self.block.rstrip(ats_string)
        elif self.block.endswith(ap_string):
            source = "AP"
            to_del_r = len(ap_string)
            self.block.rstrip(ap_string)
        else:
            print "ERROR"
            source = ""

        self.block = self.block[:-to_del_r]
        
        return source
        
    def strip_place(self, block):
        if self.source == "ATS":
            """
            regexp = compile("(.*) \(ats\) .*")
            f = findall(regexp, block)[0]
            f = descape(f)
            """
            f = ""
        elif self.source == "AP":
            regexp = compile("(.*?) \(AP\).*")
            f = findall(regexp, block)[0]
            f = descape(f)                
            
        return f    

    def strip_text(self, block):
        self.block = self.block.rstrip("</span>\n\n  \n")
        return self.block
        
        """
        if self.source == "AP":
            l = len(self.place) + 6
        elif self.source == "ATS":
            #l = len(self.place) + 6
            l = 0
            
            block = block.replace("\n \n", "**********")
            block = block.replace("\n\n", "")
            block = block.replace("**********", "")
        else:
            raise BadSourceException
                
        return block[l:]
        """

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

        self.title = self.strip_title(page)
        
        self.block = self.strip_block(page)
        #print "************", self.block
        
        
        self.source = self.strip_source()        
        #print "**", self.source

        self.place = self.strip_place(self.block)
        #print "*", self.place
        
        self.text  = self.strip_text(self.block)
        #print "***", self.text
        
        self.ts    = self.strip_timestamp(page)
        
        r = {"title":self.title, \
             "titleUp":'', \
             "titleDown":'', \
             "authors":'', \
             "place":self.place, \
             "source":self.source, \
             "time":self.ts, \
             "link":url, \
             "text":self.text, \
             "category":'Suisse'}
        
        return r;
        
    def __init__(self):
        pass
        
    def urls(self):
        
        base_url = "http://www.edicom.ch/fr/news/suisse/"
        URL = "http://www.edicom.ch/fr/news/suisse/275.html"
        
        page = urlopen(URL).read()
        
        regexp = compile("<a href=\"278_(\d\d\d\d\d\d\d)\.html\"")
        f = findall(regexp, page)

        l = []
        for u in f:
            l.append(base_url + "278_" + u + ".html")
                
        return l


if __name__ == "__main__":

    module = NM_Edicom()

    urls = module.urls()
    
    """
    urls = ["http://www.edicom.ch/fr/news/suisse/index.php?idIndex=278&idContent=1958596"]
    """

    for u in module.urls():
        print u
        print module.record(u)            
    

    #r = module.record(adresse)
    #for s in r:
    #    print s, "--> ", r[s] 
    
    
    """
    try:
        #adresse = "http://fr.news.yahoo.com/050720/5/4id24.html"
        print module.record(adresse)
    except:
        print "Exception: ", adresse
    """
    
    """
    for url in urls:
        print url
        try:
            record = module.record(url)
            #print record
            for r in record:
                print r, " ---> ", record[r]
        except:
            print "*** Exception: ", url
    """
