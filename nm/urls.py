from django.conf.urls.defaults import *
from newsmemory.nm.models import *
from newsmemory.nm import *

urlpatterns = patterns('',
    (r'^$/?',                                 'newsmemory.nm.views.news_by_day'),

    (r'^search/$',                            'newsmemory.nm.views.search'),
    (r'^log_me_out/$',                        'newsmemory.nm.views.log_me_out'),



    #(r'^flagged_news/$',                      'newsmemory.nm.views.flagged_news'),
    (r'^flaggednews/$',                       'newsmemory.nm.views.flagged_news'),

    (r'^newsmemory/index/news/$',             'django.views.generic.simple.redirect_to', {'url': '/'}),
    (r'^newsitems/(?P<object_id>\d+)/$',      'newsmemory.nm.views.newsitem'),

    (r'^flag/(?P<object_id>\d+)/$',           'newsmemory.nm.views.flag'),
    (r'^unflag/(?P<object_id>\d+)/$',         'newsmemory.nm.views.unflag'),

    (r'^24Heures/$',                          'newsmemory.nm.views.news_by_source', {'source':'24Heures', 'source_url':'24Heures'}),
    (r'^ISN/$',                               'newsmemory.nm.views.news_by_source', {'source':'ISN Security Watch', 'source_url':'ISN'}),
    (r'^LeMonde/$',                           'newsmemory.nm.views.news_by_source', {'source':'Le Monde', 'source_url':'LeMonde'}),
)
