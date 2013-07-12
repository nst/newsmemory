#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import htmlentitydefs
from urllib import *
from re import *
from myhtmlutils import *
from NM_Interface import *
from sets import *

class NM_Liberation(NM_Module):
    
    def strip_date(self, page):
        regexp = compile(".*<span class=\"art-aut\">(.*?)</span>.*")
        f = findall(regexp, page)[0]
        #print "**", f
        f = f.split("<br>")
        
        f = f[-1:][0]
        #print "-", f
        try:
            regexp = compile("(\w*) (\d{1,2}) (\S*) (\d{4}) \(Liberation\.fr - (\d\d):(\d\d)")
            #regexp = compile("(\w*) (\d{1,2}) (\S*) (\d{4})")
            f = findall(regexp, f)[0]
            #print "__", f
        except:
            try:
            
                regexp = compile("(\w*) (\d{1,2}) (\S*) (\d{4}) \(Reuters - (\d\d):(\d\d)")
                #regexp = compile("(\w*) (\d{1,2}) (\S*) (\d{4})")
                f = findall(regexp, f)[0]
                #print "__", f            
            except:
                #print "ex"
                #print f
                f = f.split(' ')
                f.append('00') # h
                f.append('00') # m
                f.append('00') # s
        
        #print ">>", f
        #f = f[0]
        
        #print "----", f
                
        day = f[1]
        month = f[2]
        year = f[3]
        h = f[4]
        m = f[5]
        
        #print month
        months = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', \
                  'juillet', 'ao&ucirc;t', 'septembre', 'octobre', 'novembre', 'décembre']
        month = str(months.index(month) + 1)
    
        if(len(month) == 1):
            month = "0" + month
        
        #print year + month + day + h + m + "00"
        
        return year + month + day + h + m + "00"

    def strip_title_up(self, page):
        regexp = compile(".*<span class=\"art-surtit\">(.*?)(<br>)?</span>.*")
        f = findall(regexp, page)[0][0]
        
        return f
    
    def strip_title(self, page):
        regexp = compile("<span class=\"art-tit\"><b>(.*?)</b></span>")
        f = findall(regexp, page)[0]
        
        return f
    
    def strip_category(self, page):
        regexp = compile("<font color=\"#666666\"><b>(.*?)</b></font>")
        f = findall(regexp, page)[0]
        
        f = f.replace('é', 'e')
        f = f.replace('è', 'e')
        
        return f
    
    def strip_authors(self, page):
        
        regexp = compile("<span class=\"art-aut\">(.*?)<br>")
        try:
            f = findall(regexp, page)[0]
            f = f.replace("&nbsp;", " ")
        except:
            f = ""    
        return f
        
    def strip_title_down(self, page):
        regexp = compile("<span class=\"art-surtit\">(.*?)</span>")
        f = findall(regexp, page)[0]
        return remove_tags(f)    
    
    def strip_text(self, page):
        #regexp = compile(".*<span class=\"art-txt\">(.*?)<span class=''>.*?</span>(.*?)</span>.*", DOTALL)
        regexp = compile(".*?<span class=\"art-txt\">(.*?)</span>.*", DOTALL)
        f = findall(regexp, page)
        
        #print f
        
        f = "".join(f[0])

        try:
            regexp = compile(".*<img src=\"/img/let/(.)\.gif.*?>.*")
            lettrine = findall(regexp, f)
            lettrine = lettrine[0].upper()
            f = f.replace("<p>", "<p>" + lettrine, 1)
        except:
            pass
        
        f = f.replace("<br />", "\n\n")        
        f = f.replace("</p><p>", "\n\n")
        
        f = remove_tags(f)
        f = f.lstrip('\n')
        #print f
        
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
                
        self.source = "Libération"
        
        self.url = url
        
        page = urlopen(url).read()

        self.titleUp   = ""#self.strip_title_up(page)
        #print "* ", self.titleUp
        
        self.title     = self.strip_title(page)
        #print "* ", self.title
        
        self.titleDown = self.strip_title_down(page)
        #print "* ", self.titleDown

        self.authors  = self.strip_authors(page)
        self.category  = self.strip_category(page)

        self.text  = self.strip_text(page)
        #print self.text
        
        self.ts = self.strip_date(page)
        
        #return "asd"
        
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
        URL = "http://www.liberation.fr/"
        
        page = urlopen(URL).read()
        
        regexp = compile("page.php\?Article=(\d\d\d\d\d\d)")
        f = findall(regexp, page)
        
        set = Set()
        
        for u in f:
            if u != '149907':
                set.add("http://www.liberation.fr/imprimer.php?Article=" + u)
        
        rubriques = ['SOCIETE', 'ECONOMIE', 'POLITIQUES', 'TERRE', 'MEDIAS', 'SPORTS', 'VOUS', 'CULTURE', 'GRANDANGLE', 'PORTRAITS', 'MULTIMEDIA', 'COURRIER', 'SCIENCES', 'CHATS', 'WEEKEND', 'TELEVISION', 'VOYAGES']
        
        for rub in rubriques:
        
            URL = "http://www.liberation.fr/page.php?Rubrique=" + rub
            
            page = urlopen(URL).read()
            
            regexp = compile("page.php\?Article=(\d\d\d\d\d\d)")
            f = findall(regexp, page)
                        
            for u in f:
                if u != '149907':
                    set.add("http://www.liberation.fr/imprimer.php?Article=" + u)
        
        return list(set)

if __name__ == "__main__":

    module = NM_Liberation()

    #urls = ["http://www.liberation.fr/imprimer.php?Article=294713"]
    #urls = ["http://www.liberation.fr/imprimer.php?Article=319699"]
    #urls = ['http://www.liberation.fr/imprimer.php?Article=319697']
    #urls = ['http://www.liberation.fr/imprimer.php?Article=319781']
    #urls = ["http://www.liberation.fr/imprimer.php?Article=319687"]
    #urls = ['http://www.liberation.fr/imprimer.php?Article=319816']
    #urls = ['http://www.liberation.fr/imprimer.php?Article=354954']
    urls = ['http://www.liberation.fr/imprimer.php?Article=354997']
    
    
    
    #urls = module.urls()
    
    for url in urls:
        #print "\n-------------------------------------------------------------------\n"
        #print url
        record = module.record(url)
        #print record["link"]
        for f in record:
            print f, " ---> ", record[f]
        """
        try:
            #record = module.record(url)
            #print record
            record = module.record(url)
            print record["link"]
        except:
            print "Exception: ", url
        """



