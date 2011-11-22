from django.conf.urls.defaults import *
#from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns(
    'upforit.views',
    (r'^$',  'upforit_view'),
    (r'^login/$', 'login_view'),
    (r'^register/$', 'register_view'),
    (r'^logout/$', 'logout_view'),
    (r'^new_recipe/$', 'new_recipe_view'),
    (r'^delete_recipe/$', 'delete_recipe_view'),
)
