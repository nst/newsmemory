#!/usr/bin/python

import htmlentitydefs
import re

pattern = re.compile("&(\w+?);")

def remove_tags(data):
    text = re.sub('<!--.*?-->', '', data) #Remove comments first, or '>' in
                                          #comments will be interpreted as
                                          #end of (comment) tag.
    data = re.sub('<.*?>', '', text)
    return data

def descape_entity(m, defs=htmlentitydefs.entitydefs):
    # callback: translate one entity to its ISO Latin value
    try:
        return defs[m.group(1)]
    except KeyError:
        return m.group(0) # use as is

def descape(string):
    string = string.replace("&#039;", "'")
    return pattern.sub(descape_entity, string)
