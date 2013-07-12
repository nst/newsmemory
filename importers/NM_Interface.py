#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

"""
Extend NM_Interface to build a News Memory module.
Ask seriot@seriot.ch for anything you'd like to add.
Have fun!
"""

class BadSourceException(Exception):
    """
    Raised in case an URL does not match a regular source.
    """
    def __str__(self):
        return "BadSourceException"

class NM_Module:
    """
    You've got two methods to inherit from.
    
    Please read the records comments carefuly,
    or your module might not work.
    
    Email seriot@seriot.ch for questions.
    """
    
    def record(self, url):
        """
        builds the record from an url
        """
        
        r = {"title":"",       # article title
             "titleUp":"",     # hat
             "titleDown":"",   # subtitle
             "place":"",       # Paris, Berlin, ...
             "source":"",      # AFP, Le Figaro, 24Heures, ...
             "time":"",        # YYYYMMDDHHMMSS
             "link":url,       # article link
             "text":"",        # article body
             "category":"9",   #
             "authors":""}     # 
        
        return r;
    
    def urls(self):
        return [] # a list of article links

if __name__ == "__main__":

    module = NM_Module()
    
    print module

    #module = NM_My_Module()

    #print module.urls()
    
    #url = "http://link_to_my_article.foo/index.php?article_id=123"
    #print module.record(url)
 