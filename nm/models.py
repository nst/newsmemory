from django.db import models
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User

from search import SearchManager 

import os
import datetime

# Create your models here.

class Category(models.Model):
    name = models.CharField(maxlength=100, blank=True)
    
    def __str__(self):
        return self.name

    class Admin:
        pass

class Country(models.Model):
    code = models.CharField(maxlength=2, primary_key=True)
    name_fr = models.CharField(maxlength=100, blank=True)

    def __str__(self):
        return self.name_fr

    class Admin:
        pass

class Place(models.Model):
    name = models.CharField(maxlength=200, unique=True)
    country = models.ForeignKey(Country, db_column='country', to_field="code", maxlength=2, blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Admin:
        pass

class Source(models.Model):
    TYPES = (
        ('a', 'Agency'),
        ('p', 'Paper'),
        ('w', 'Web'),
        ('u', 'Unknown')
    )
    
    LANGUAGES = (
        ('en', 'English'),
        ('fr', 'French')
    )
    
    name = models.CharField(maxlength=200, blank=True)
    url = models.CharField(maxlength=200, blank=True)
    info = models.TextField(blank=True)
    type = models.CharField(maxlength=1, choices=TYPES)
    language = models.CharField(maxlength=2, choices=LANGUAGES, default='u')
    country = models.ForeignKey(Country, db_column='country', to_field="code", maxlength=2, blank=True, null=True)
    logo = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    def image(self):
        if self.logo:
            return settings.MEDIA_URL + os.sep + "site_media" + os.sep + self.logo
        else:
            return None
        
    class Admin:
        pass

class Newsitem(models.Model):
    titleUp = models.CharField(maxlength=200, blank=True)
    title = models.TextField(blank=True)
    titleDown = models.TextField(blank=True)
    text = models.TextField(blank=True)
    link = models.CharField(maxlength=200, blank=True, unique=True)
    time = models.DateTimeField(null=True)
    source = models.ForeignKey(Source, db_column='source', blank=True)
    place = models.ForeignKey(Place, db_column='place', blank=True, null=True)
    category = models.ForeignKey(Category, db_column='category', blank=True, null=True)
    authors = models.TextField(blank=True)

    objects = SearchManager('text')

    #def save(self):
        #try:
        #super(Text, self).save() # Call the "real" save() method.
        #except:
        #    pass

    def __str__(self):
        return self.title
    
    def pretty_time(self):
        s = "%s" % self.time
        return s[:-3]

    def get_absolute_url(self):
        return "/newsitems/%i/" % self.id

    def is_flagged(self):
        qs = Log.objects.filter(newsitem=self.id, marked=True)
        return qs.count() > 0

    class Admin:
        list_display = ('time', 'source', 'title')
        ordering = ['-time']

class Log(models.Model):
    user = models.ForeignKey(User)
    newsitem = models.ForeignKey(Newsitem)
    marked = models.BooleanField()
    
    def __str__(self):
        return "%s %s %s" % (self.user, self.newsitem, self.marked)
    
    class Meta:
        unique_together = (("user", "newsitem"),)
    
    class Admin:
        pass
