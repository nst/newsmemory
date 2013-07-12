#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# Swissinfo

import htmlentitydefs
from urllib import *
from re import *
from myhtmlutils import *
from NM_Interface import *
from sys import *

class NM_Swissinfo(NM_Module):
    """
    Module pour les rubriques "suisse" et "international" de Swissinfo
    http://www.swissinfo.org/sfr/swissinfo.html?siteSect=100
    """
    
    def date_to_timestamp(self, date):
        date = date.split(' ')
                
        day = date[0]
        year = date[2]
        months = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', \
                  'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
        month = str(months.index(date[1]) + 1)
    
        if(len(day) == 1):
            day = "0" + day

        if(len(month) == 1):
            month = "0" + month
        
        (hours, minutes) = date[3].split(':')
        
        if(len(hours) == 1):
            hours = "0" + hours
        
        seconds = "00"
        
        return year + str(month) + day + hours + minutes + seconds
    
    def strip_title(self, page):
        regexp = compile("<div class=\"s00\">(.*?)</div>")
        f = findall(regexp, page)[0]
        
        return f
    
    def strip_block_ats(self, page):
        regexp = compile("<div class=\"l02\">(.*?)</div>")
        f = findall(regexp, page)[0]
        
        f = f.replace("<br>", "\n")
        
        return f
    
    def strip_date(self, page):
        regexp = compile("<div class=\"t01\">(.*?)</div>")
        f = findall(regexp, page)[0]
        
        return f
    
    def strip_place(self, block):
        regexp = compile("(.*?) - .*")
        f = findall(regexp, block)
        
        #print f
        
        if f:
            return f[0]
        else:
            return ""
            
    def strip_source(self):
        return "ATS"
    
    def strip_text(self, block):
        place_len = len(self.place)
        
        if(place_len):
            to_del = place_len + 3
    
        return block[to_del:]

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

        self.source = "ATS"
        
        self.url = url

        strip_block = self.strip_block_ats(page)
        
        self.title = self.strip_title(page)
        
        self.block = self.strip_block_ats(page)
        
        self.place = self.strip_place(self.block)
        
        self.text  = self.strip_text(self.block)
        
        self.ts    = self.date_to_timestamp(self.strip_date(page))
        
        r = {"title":self.title, \
             "titleUp":'', \
             "titleDown":'', \
             "place":self.place, \
             "source":self.source, \
             "time":self.ts, \
             "link":self.url, \
             "text":self.text, \
             "category":"monde", \
             "authors":""}
        
        return r;
        
    def __init__(self):
        pass
        
    def urls(self):
        URL = "http://www.swissinfo.org/sfr/swissinfo.html?siteSect="
        
        rep = "142" # international
        
        page = urlopen(URL + rep).read()
        
        regexp = compile(".*siteSect=(\d*)&amp;sid=(\d*).*")
        f = findall(regexp, page)
        
        d = {}
        for (siteSect, sid) in f:
            if siteSect in ['113', '143']:
                d[(siteSect, sid)] = None
        
        f = d.keys()
        
        l = []
        for (siteSect, sid) in f:
            l.append("http://www.swissinfo.org/sfr/swissinfo.html?siteSect=" + siteSect + "&sid=" + sid)
                
        return l


if __name__ == "__main__":

    module = NM_Swissinfo()

    adresse = "http://www.swissinfo.org/sfr/swissinfo.html?siteSect=143&sid=64306590"
    print module.record(adresse)

    """
    try:
        #adresse = "http://fr.news.yahoo.com/050720/5/4id24.html"
        print module.record(adresse)
    except:
        print "Exception: ", adresse
    """
    
    """
    urls = module.urls()
    #print urls
    for url in urls:
        print url
        try:
            record = module.record(url)
            print record
        except:
            print "Exception: ", url
    """
