from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
    # Example:
    
     (r'^', include('newsmemory.nm.urls')),
     (r'^$/', include('newsmemory.nm.urls')),

     (r'^admin/', include('django.contrib.admin.urls')),

     (r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

     (r'^accounts/login/$', 'django.contrib.auth.views.login'),
     (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
     (r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
)
