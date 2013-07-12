#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#from DB import *
#import htmlentitydefs
from urllib import *
from re import *
from myhtmlutils import *
from NM_Interface import *
#from sys import *

class NM_ISN(NM_Module):
    """
    Module pour ISN
    """
    
    def strip_date(self, page):
        regexp = compile(".*<p>(.*?)</p>.*")
        f = findall(regexp, page)[0]
        #print f
        
        f = f.split(' ')
        #print f
        
        day = f[0]
        month = f[1]
        year = f[2]
        
        months = ['January', 'February', 'March', 'April', 'May', 'June', \
                  'July', 'August', 'September', 'October', 'November', 'December']
        month = str(months.index(month) + 1)
    
        if(len(month) == 1):
            month = "0" + month

        hms = "000000"


        
        if self.title.startswith("News Briefs"):
            title = self.title
            try:
                regexp = compile(".*(\d\d).(\d\d).?GMT.*")
                f = findall(regexp, title)
                f = f[0]
                hms = ''.join(f) + "00"
            except:
                pass
        else:
            try:
                regexp = compile(".*(\d\d).(\d\d) GMT.*")
                f = findall(regexp, page)[0]
                hms = ''.join(f) + "00"
            except:
                pass
        
        return year + month + day + hms
    
    def strip_title(self, page):
        regexp = compile(".*?<h1>(.*?)</h1>.*")
        
        #print findall(regexp, page)
        
        f = findall(regexp, page)[0]
        
        return f
    
    def strip_title_down(self, page):
        regexp = compile(".*?<p><strong>(.*?)</strong></p>.*", DOTALL)
        
        try:
            f = findall(regexp, page)[0]
            return f
        except:
            return ""
       
    def strip_text(self, page):
        regexp = compile(".*<p class=\"readable\">(.*)</p>.*", DOTALL)
        f = findall(regexp, page)
        
        if isinstance(f, type([])):
            f = f[0]

        f = f.replace("<p><b>", "\r\n")
        f = f.replace("</b></p>", "\r\n")

        f = remove_tags(f)

        i = 0
        if f.startswith("ISN"):
            # search unicode dash
            i = f.find("\xe2\x80\x93")
            
            # if found
            if i != -1:
                f = f[i+4:]
            else: # if not found
                i = f.find("-") # search ascii dash
                f = f[i+2:]
                
        #f = "<P>" + f + "</P>"

        f = f.replace("\r\n\r\n", "\r\n")

        #f = f.replace("\r\n", "</P>\n\n<P>")
        f = f.replace("\r\n", "\n\n")


        f = f.replace("<P></P>", "") # weird

        f = f.lstrip('\n')
        
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
        
        page = urlopen(url).read()
        
        page = page.replace("\xe2\x80\x98", "'")
        page = page.replace("\xe2\x80\x99", "'")
        page = page.replace("\xe2\x80\x9c", '"')
        page = page.replace("\xe2\x80\x9d", '"')
        page = page.replace("\xc3\xb6", 'ö')
        
        self.source = "ISN Security Watch"
                
        self.url = url
        
        self.title = self.strip_title(page)

        self.text  = self.strip_text(page)
        
        self.titleDown = self.strip_title_down(page)
        
        self.ts = self.strip_date(page)
        
        r = {"title":self.title,
             "titleUp":"",
             "titleDown":self.titleDown,
             "place":"",
             "source":self.source,
             "time":self.ts,
             "link":self.url,
             "text":self.text,
             "category":"Monde",
             "authors":""}
        
        return r
    
    def __init__(self):
        pass
        
    def urls(self):
        
        URL = "http://www.isn.ethz.ch/news/sw/last_5_days.cfm"
        base_url = "http://www.isn.ethz.ch/news/sw/details_print.cfm?id="
                
        page = urlopen(URL).read()
        
        regexp = compile(".*details.cfm\?id=(\d*).*")
        f = findall(regexp, page)
        
        d = {}
        for i in f:
            d[i] = ""
        
        f = d.keys()
            
        l = []
        for u in f:
            l.append(base_url + u)
                
        return l

if __name__ == "__main__":

    db = DB()
    module = NM_ISN()

    #urls = module.urls()
    
    urls = []
    for x in [10966, 10865, 10833]:
        urls.append("http://www.isn.ethz.ch/news/sw/details_print.cfm?id=%d" % x)

    print urls
    
    for url in urls:
        if db.url_in_db(url):
            print "in db : %s" % url
        else:
            try:
                r = module.record(url)

                if r:
                    db.add_news(r)
                    
                    for field in r:
                        print "%s ---> %s" % (field, r[field])

            except:
                print "Exception: ", url
