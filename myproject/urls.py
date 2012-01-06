#from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.defaults import *
#from django.contrib.auth.views import login, logout
#from myproject import settings

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    (r'^',  include('inkle.urls')),
)
