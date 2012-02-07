from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
#from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns(
    "myproject.inkle.views",
    (r"^$", "home_view"),
    (r"^login/$", "login_view"),
    (r"^register/$", "register_view"),
    (r"^verifyEmail/(?P<email>.+)/(?P<verification_hash>\w+)/$", "verify_email_view"),
    (r"^requestPasswordReset/$", direct_to_template, { "template" : "requestPasswordReset.html" }),
    (r"^passwordResetConfirmation/(?P<email>.+)/$", direct_to_template, { "template" : "passwordResetConfirmation.html" }),

    (r"^sendEmailVerificationEmail/(?P<email>.+)/$", "send_email_verification_email_view"),
    (r"^sendUpdateEmailVerificationEmail/(?P<email>.+)/$", "send_update_email_verification_email_view"),
    (r"^sendPasswordResetEmail/(?P<email>.+)/$", "send_password_reset_email_view"),
    (r"^sendRequestToFollowEmail/(?P<to_member_id>\w+)/$", "send_request_to_follow_email_view"),
    (r"^sendAcceptRequestEmail/(?P<from_member_id>\w+)/$", "send_accept_request_email_view"),
    (r"^sendInklingInvitationEmail/$", "send_inkling_invitation_email_view"),
    
    (r"^dateSelect/$", "date_selected_view"),
    
    (r"^resetPassword/(?P<email>.+)/(?P<verification_hash>\w+)/$", "reset_password_view"),
    (r"^resetPassword/$", "set_password_view"),
    (r"^logout/$", "logout_view"),
    (r"^editMember/$", "edit_member_view"),
    
    (r"^editLocation/$", "edit_location_view"),
    (r"^getEditLocationHtml/$", "get_edit_location_html_view"),
    (r"^getEditManageHtml/$", "get_edit_manage_html_view"),
    
    # Search views
    (r"^search/(?P<query>.+)/$", "search_view"),
    (r"^getSearchContent/$", "get_search_content_view"),
    
    (r"^suggestions/$", "suggestions_view"),   
    (r"^requestToFollow/$", "request_to_follow_view"),
    (r"^revokeRequest/$", "revoke_request_view"),
    (r"^acceptRequest/$", "accept_request_view"),
    (r"^rejectRequest/$", "reject_request_view"),
    (r"^preventFollowing/$", "prevent_following_view"),
    
    (r"^stopFollowing/$", "stop_following_view"),


    (r"^inklingInvitations/$", "inkling_invitations_view"),

    (r"^inviteToInkle/$", "invite_to_inkle_view"),

    # Manage page
    (r"^manage/$", "manage_view"),
    (r"^manage/(?P<content_type>notifications|place|blots|networks|followers)/$", "manage_view"),
    (r"^manage/(?P<content_type>place)/(?P<date>\d\d?_\d\d?_\d\d\d\d)/$", "manage_view"),
    (r"^manage/(?P<content_type>place)/(?P<date>\d\d?_\d\d?_\d\d\d\d)/(?P<place_type>all|dinner|pregame|mainEvent)/$", "manage_view"),
    #Manage page database views
    (r"^notifications/$", "notifications_view"),
    (r"^place/$", "get_member_place_view"),
    (r"^blots/$", "blots_view"),
    (r"^networks/$", "networks_view"),
    (r"^followers/$", "followers_view"),

    (r"^blots/(?P<blot_id>\w+)/$", "blots_view"),
    (r"^createBlot/$", "create_blot_view"),
    (r"^renameBlot/$", "rename_blot_view"),
    (r"^deleteBlot/$", "delete_blot_view"),
    (r"^removeFromBlot/$", "remove_from_blot_view"),
    (r"^addToBlot/$", "add_to_blot_view"),
    
    
    (r"^joinNetwork/$", "join_network_view"),
    (r"^leaveNetwork/$", "leave_network_view"),

    # Invitation response
    (r"^invitationResponse/$", "invitation_response_view"),
    
    (r"^createInkling/$", "create_inkling_view"),
    (r"^removeInkling/$", "remove_inkling_view"),
    (r"^getMyInklings/$", "get_my_inklings_view"),
    (r"^createNetwork/$", "create_network_view"),
    (r"^createLocation/$", "create_location_view"),
    (r"^getOthersInklings/$", "get_others_inklings_view"),
    (r"^uploadImage/$", "upload_image_view"),
    
    #Member page
    (r"^member/(?P<other_member_id>\d+)/$", "member_view"),
    #urls to load default member content
    (r"^member/(?P<other_member_id>\d+)/(?P<content_type>inklings|place|networks|following|followers)/$", "member_view"),
    (r"^member/(?P<other_member_id>\d+)/(?P<content_type>inklings|place)/(?P<date>\d\d?_\d\d?_\d\d\d\d)/$", "member_view"),
    (r"^member/(?P<other_member_id>\d+)/(?P<content_type>inklings|place)/(?P<date>\d\d?_\d\d?_\d\d\d\d)/(?P<place_type>all|dinner|pregame|mainEvent)/$", "member_view"),
    #Database view content loading for member page
    (r"^getMemberInklings/$", "get_member_inklings_view"),
    (r"^getMemberPlace/$", "get_member_place_view"),
    (r"^getMemberNetworks/$", "networks_view"),
    (r"^getMemberFollowing/$", "get_member_following_view"),
    (r"^getMemberFollowers/$", "followers_view"),
    
    #Location page
    (r"^location/(?P<location_id>\d+)/$", "location_view"),
    #urls to load default location content
    (r"^location/(?P<location_id>\d+)/(?P<content_type>all|dinner|pregame|mainEvent)/$", "location_view"),
    (r"^location/(?P<location_id>\d+)/(?P<content_type>all|dinner|pregame|mainEvent)/(?P<date>\d\d?_\d\d?_\d\d\d\d)/$", "location_view"),
    (r"^location/(?P<location_id>\d+)/(?P<date>\d\d?_\d\d?_\d\d\d\d)/$", "location_view"),
    #Database view content loading for location page
    (r"^getLocationInklings/$", "get_location_inklings_view"),
    
    (r"^network/(?P<network_id>\d+)/$", "network_view"),

    (r"^account/$", "account_view"),
    (r"^account/(?P<content_type>password|email|deactivate)/$", "account_view"),
    (r"^resetAccountPassword/$", "reset_account_password_view"),
    (r"^updateAccountEmail/$", "update_account_email_view"),
    (r"^deactivateAccount/$", "deactivate_account_view"),

    (r"^editProfile/$", "edit_profile_view"),
    (r"^editProfile/(?P<content_type>information|picture|privacy|emailPreferences)/$", "edit_profile_view"),
    (r"^editProfileInformation/$", "edit_profile_information_view"),
    (r"^editProfilePicture/$", "edit_profile_picture_view"),
    (r"^editProfilePrivacy/$", "edit_profile_privacy_view"),
    (r"^editProfileEmailPreferences/$", "edit_profile_email_preferences_view"),
    (r"^editProfilePicture/$", "edit_profile_picture_view"),
    (r"^getNewProfilePicture/$", "get_new_profile_picture_view"),

    (r"^terms/$", "terms_view"),
    (r"^contact/$", "contact_view"),
    (r"^sendContactEmail/$", "send_contact_email_view"),
    (r"^help/$", "help_view"),
    (r"^help/(?P<content_type>overview|home|following|blots|networks|inklings|places)/$", "help_view"),
)
