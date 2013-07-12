# -*- coding: utf-8 -*-

from django import template
from django.conf import settings

import re
import locale
import datetime

def highlight(value, q):
    #return value.replace(q, '<span class="highlight">%s</span>' % q)

    regexp = re.compile(q, re.IGNORECASE)
    return re.sub(regexp, '<span class="highlight">%s</span>' % q, value)

def flagged_icon(value):
    if value:
        return '<img src="/site_media/flag.png">'
    else:
        return ''

def french_date(value):
    if value == None:
        return "[date non renseignée]"
        
    locale.setlocale(locale.LC_ALL, 'fr_FR')
    return value.strftime("%A %d %B %Y")

def french_datetime(value):
    if value == None:
        return "[date non renseignée]"

    locale.setlocale(locale.LC_ALL, 'fr_FR')
    return value.strftime("%A %d %B %Y, %H:%M")
    
register = template.Library()

register.filter('highlight', highlight)
register.filter('french_date', french_date)
register.filter('flagged_icon', flagged_icon)
register.filter('french_datetime', french_datetime)
