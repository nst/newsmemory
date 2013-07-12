#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from NM_Interface import *
import htmlentitydefs
from urllib2 import *
from re import *
from myhtmlutils import *
#from NM_Interface import *
from sys import *
from dTr import *

class NM_Diplo(NM_Module):
    
    def strip_date(self, page):
        regexp = compile(".*<meta name=\"Date\" content=\"(\d\d\d\d)-(\d\d).*")
        
        f = findall(regexp, page)
        return f[0][0] + f[0][1] + "01000000"
    
    def strip_title(self, page):
        regexp = compile(".*<title>(.*?)</title>.*")
        f = findall(regexp, page)[0]
        
        return f
    

    def strip_title_up(self, page):
        regexp = compile(".*<span class=\"diplo-surtitre\">(.*?)</span>.*")
        try:
            f = findall(regexp, page)[0]
            f = descape(f)
            f = remove_tags(f)
            return f
        except:
            return ""    
    
    
    def strip_title_down(self, page):
        regexp = compile(".*<B>\n<p class='spip' align='justify'>(.*?)</p>\n</B>.*", DOTALL)
        try:
            #print findall(regexp, page)
            f = findall(regexp, page)[0]

            f = descape(f)
            f = remove_tags(f)
            return f
        except:
            return ""
        

    def strip_author(self, page):
        r = ""

        afull = []

        try:
            regexp = compile(".*<P><B>(.*?)</B><FONT COLOR=\"#666666\"><BR>(.*?)</FONT>.*")
            
            f = findall(regexp, page)
            
            for i in f:
                r += i[0] + " -- " + i[1] + "\n\n"
                afull.append(i[0])
            
            r = descape(r)
            r = remove_tags(r)
        except:
            pass


        try:
            regexp = compile(".*<P><B>(.*?)</B>.*")
            
            f = findall(regexp, page)
            
            for i in f:
                if i not in afull:
                    r += i + "\n\n"
            
            r = descape(r)
            r = remove_tags(r)
        
        except:
            pass



        """
        try:
            regexp = compile(".*<P><B>(.*?)</B><FONT COLOR=\"#666666\"><BR>(.*?)</FONT>.*")
            
            f = findall(regexp, page)
            
            for i in f:
                r += i[0] + " -- " + i[1] + "\n"
            
            r = descape(r)
            r = remove_tags(r)
        except:
            pass

        if r == "":
            try:
            
                regexp = compile(".*<P><B>(.*?)</B>.*")
                
                f = findall(regexp, page)
                
                for i in f:
                    r += i + "\n"
                
                r = descape(r)
                r = remove_tags(r)
            
            except:
                pass
        """

        return r
    
    def strip_text(self, page):
        regexp = compile(".*\n\n\n<p class=((\")|('))spip((\")|(')) align='justify'>\n?(.*)</p>\n\n\n.*", DOTALL)
        
        f = findall(regexp, page)
        
        s = f[0][6]
        
        s = s.replace("<p class=\"spip\" align='justify'>", "\n")
        s = s.replace("<h3 align=center>", "\n")
                
        #s = s.replace("\n", "___")
        #s = s.replace("______", "\n")
        #s = s.replace("___", "")
        
        s = descape(s)
        s = remove_tags(s)
        
        return s

    def strip_notes(self, page):
        #print page
        
        regexp = compile("<p class=\"spip_note\">\n?(.*?)</p>", DOTALL)

        f = findall(regexp, page)

        #print f
        
        f = "$£".join(f)

        f = remove_tags(f)
        
        f = f.replace("$£", "<BR>\n")

        f = descape(f)
        #f = remove_tags(f)
        
        return f

    block  = ""

    title  = ""
    place  = ""
    text   = ""
    source = ""
    ts     = ""
    url    = ""
    
    subject = ""
    
    def urls(self):
        
        f = open("/diplo_list.txt").readlines()
        
        l = []
        
        for line in f:
            l.append(line[:-1])
            
        return l
        #return ['http://www.monde-diplomatique.fr/2003/03/BESSIS/9971']
                
    def record(self, url):
        """
        construit un record à partir d'un url
        """
        
        page = urlopen(url).read()
        
        page = strTr(page, d)
        
        self.source = "Le Monde Diplomatique"
        
        self.url = url

        self.titleUp = self.strip_title_up(page)
        
        self.title = self.strip_title(page)
        
        self.titleDown = self.strip_title_down(page)

        self.authors = self.strip_author(page)

        self.text = self.strip_text(page)
        self.text += "\n\n\n" + self.strip_notes(page)
        
        self.ts = self.strip_date(page)

        #z = self.strip_author(page)
        
        r = {"title":self.title, \
             "titleUp":self.titleUp, \
             "titleDown":self.titleDown, \
             'authors':self.authors, \
             "place":self.place, \
             "source":self.source, \
             "time":self.ts, \
             "link":self.url, \
             "text":self.text, \
             "category":'divers'}
        
        return r;
    
    def __init__(self):
        pass

if __name__ == "__main__":

    module = NM_Diplo()
    
    urls = module.urls()
    
    #print urls
    
    #urls = ["http://www.monde-diplomatique.fr/1984/04/JULIEN/12260"]
    #urls = ["http://www.monde-diplomatique.fr/2000/05/LAIME/13720"]
    #urls = ["http://www.monde-diplomatique.fr/2002/01/DA_SILVA/16004"]
    #urls = ["http://www.monde-diplomatique.fr/1997/07/EDELMAN/8838"]
    #urls = ["http://www.monde-diplomatique.fr/1989/08/HALIMI/"]
    #urls = ["http://www.monde-diplomatique.fr/1981/06/RAMEDHAN/11853"]
    #urls = ["http://www.monde-diplomatique.fr/1989/10/JULIEN/12265"]
    """
    for url in urls:
    
        record = module.record(url)
        for k in record:
            print k, " --> " + record[k]
    """
    
        
    for url in urls:
        try:
            #record = module.record(url)
            print "x ", url
            #for k in record:
            #    print k, " --> " + record[k]
        except:
            print "  ", url

