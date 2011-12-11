from django.conf.urls.defaults import *
#from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns(
    "inkle.views",
    (r"^$", "home_view"),
    (r"^login/$", "login_view"),
    (r"^logout/$", "logout_view"),
    (r"^editProfile/$", "edit_profile_view"),
    (r"^location/(?P<location_id>\d+)/$", "location_view"),
    (r"^location/(?P<location_id>\d+)/edit/$", "edit_location_view"),
    (r"^location/(?P<location_id>\d+)/edit/(?P<name>\w+)/(?P<street>\w+)/(?P<city>\w+)/(?P<state>\w+)/(?P<zip_code>\d+)/(?P<category>\w+)/$", "edit_location_view2"),
    (r"^manage/$", "manage_view"),
    (r"^search/(?P<query>.+)/$", "search_view"),
    (r"^requested/$", "requested_view"),
    (r"^spheres/$", "spheres_view"),
    (r"^followers/$", "followers_view"),
    (r"^followRequest/$", "follow_request_view"),
    (r"^revokeRequest/$", "revoke_request_view"),
    (r"^acceptRequest/$", "accept_request_view"),
    (r"^rejectRequest/$", "reject_request_view"),
    (r"^preventFollowing/$", "prevent_following_view"),
    (r"^removeFromCircle/$", "remove_from_circle_view"),
    (r"^addToCircle/$", "add_to_circle_view"),
    (r"^stopFollowing/$", "stop_following_view"),
    (r"^circles/$", "circles_view"),
    (r"^circleContent/$", "circle_content_view"),
    (r"^addCircle/$", "add_circle_view"),
    (r"^deleteCircle/$", "delete_circle_view"),
    (r"^joinSphere/$", "join_sphere_view"),
    (r"^leaveSphere/$", "leave_sphere_view"),
    (r"^suggestions/$", "suggestions_view"),
    (r"^setInkling/$", "set_inkling_view"),
    (r"^getInklings/$", "get_inklings_view"),
)
