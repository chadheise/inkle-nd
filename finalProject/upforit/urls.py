from django.conf.urls.defaults import *
#from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns(
    "upforit.views",
    (r"^$", "home_view"),
    (r"^login/$", "login_view"),
    (r"^register/$", "register_view"),
    (r"^logout/$", "logout_view"),
    (r"^location/(?P<location_id>\d+)/$", "location_view"),
    (r"^location/(?P<location_id>\d+)/edit/$", "edit_location_view"),
    (r"^location/(?P<location_id>\d+)/edit/(?P<name>\w+)/(?P<street>\w+)/(?P<city>\w+)/(?P<state>\w+)/(?P<zip_code>\d+)/(?P<category>\w+)/$", "edit_location_view2"),
    (r"^people/$", "people_view"),
)
