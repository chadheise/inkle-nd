from django.conf.urls.defaults import *
#from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns(
    "inkle.views",
    (r"^$", "home_view"),
    (r"^login/$", "login_view"),
    (r"^register/$", "register_view"),
    (r"^logout/$", "logout_view"),
    (r"^editProfile/$", "edit_profile_view"),
    (r"^location/(?P<location_id>\d+)/$", "location_view"),
    (r"^editLocation/$", "edit_location_view"),
    (r"^manage/$", "manage_view"),
    (r"^manage/(?P<defaultContent>requests|circles|spheres|followers)/$", "manage_view"),
    (r"^search/(?P<query>.+)/$", "search_view"),
    (r"^requests/$", "requests_view"),
    (r"^spheres/$", "spheres_view"),
    (r"^followers/$", "followers_view"),
    (r"^requestToFollow/$", "request_to_follow_view"),
    (r"^revokeRequest/$", "revoke_request_view"),
    (r"^acceptRequest/$", "accept_request_view"),
    (r"^rejectRequest/$", "reject_request_view"),
    (r"^preventFollowing/$", "prevent_following_view"),
    (r"^removeFromCircle/$", "remove_from_circle_view"),
    (r"^addToCircle/$", "add_to_circle_view"),
    (r"^stopFollowing/$", "stop_following_view"),
    (r"^circles/$", "circles_view"),
    (r"^circleContent/$", "circle_content_view"),
    (r"^createCircle/$", "create_circle_view"),
    (r"^deleteCircle/$", "delete_circle_view"),
    (r"^joinSphere/$", "join_sphere_view"),
    (r"^leaveSphere/$", "leave_sphere_view"),
    (r"^suggestions/$", "suggestions_view"),
    (r"^createInkling/$", "create_inkling_view"),
    (r"^removeInkling/$", "remove_inkling_view"),
    (r"^getInklings/$", "get_inklings_view"),
    (r"^createSphere/$", "create_sphere_view"),
    (r"^createLocation/$", "create_location_view"),
    (r"^getOthersInklings/$", "get_others_inklings_view"),
)
