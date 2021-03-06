from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.shortcuts import render_to_response

from django.contrib.auth.models import User
from django.contrib import auth

from myproject.inkle.models import *
from myproject.inkle.emails import *

from django.db.models import Q

import datetime
import shutil

from databaseViews import *

from myproject.settings import MEDIA_ROOT

def home_view(request):
    """Gets dates objects and others' inkling locations and returns the HTML for the home page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except (Member.DoesNotExist, KeyError) as e:
        return HttpResponseRedirect("/login/")
    
    # Get date objects
    today = datetime.date.today()
    dates = [today + datetime.timedelta(days = x) for x in range(5)] 

    # Get others' dinner inklings for today
    locations = get_others_inklings(member, today, "other", "blots", "mainEvent")

    return render_to_response( "home.html",
        { "member" : member, "locations" : locations, "dates" : dates, "selectedDate" : today },
        context_instance = RequestContext(request) )

def manage_view(request, content_type = "blots", date = "today", place_type = "all"):
    """Returns the HTML for the manage page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/?next=/manage/" + content_type + "/")

    # Get date objects
    if date == "today":
        date1 = datetime.date.today()
    else:
        try:
            date1 = datetime.date(int(date.split("_")[2]), int(date.split("_")[0]), int(date.split("_")[1]) )
        except:
            date1 = datetime.date.today()
    dates = [date1 + datetime.timedelta(days = x) for x in range(3)]

    return render_to_response( "manage.html",
        {"member" : member, "dates" : dates, "selectedDate" : date1, "defaultContentType" : content_type, "place_type" : place_type},
        context_instance = RequestContext(request) )

def member_view(request, other_member_id = None, content_type = "inklings", date = "today", place_type = "all"):
    """Returns the HTML for the member page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        if (other_member_id):
            return HttpResponseRedirect("/login/?next=/member/" + other_member_id + "/")
        else:
            if content_type == "place":
                return HttpResponseRedirect("/login/?next=/manage/place/")
            else:
                return HttpResponseRedirect("/login/?next=/manage/")
    
    # Get the member whose page is being viewed (or throw a 404 error if their member ID is invalid)
    try:
        other_member = Member.active.get(pk = other_member_id)
    except:
        raise Http404()

    # Redirect the logged in member to their profile page if they are the other member
    if (member == other_member):
        redirectPath = "/manage/"
        if (content_type == "place" or content_type == "networks" or content_type == "followers"):
            redirectPath = redirectPath + content_type + "/"
            if (date != "today"):
                redirectPath = redirectPath + date + "/"
                if (content_type == "place"):
                    redirectPath = redirectPath + place_type +"/"
        return HttpResponseRedirect(redirectPath)

    # Determine the privacy rating for the logged in member and the current member whose page is being viewed
    other_member.privacy = get_privacy(member, other_member)
    
    # Create the button lists
    other_member.button_list = []

    if (member in other_member.followers.all()):
        other_member.button_list.append(buttonDictionary["blots"])
        other_member.button_list.append(buttonDictionary["stop"])
    else:
        other_member.button_list.append(buttonDictionary["request"])

    if (member in other_member.following.all()):
        other_member.button_list.append(buttonDictionary["prevent"])

    # Get date objects
    if date == "today":
        date1 = datetime.date.today()
    else:
        try:
            date1 = datetime.date(int(date.split("_")[2]), int(date.split("_")[0]), int(date.split("_")[1]) )
        except:
            date1 = datetime.date.today()
    dates = [date1 + datetime.timedelta(days = x) for x in range(3)]

    return render_to_response( "member.html",
        { "member" : member, "other_member" : other_member, "dates" : dates, "selectedDate" : date1, "content_type" : content_type, "place_type" : place_type },
        context_instance = RequestContext(request) )
    

def account_view(request, content_type = "password"):
    """Returns the HTML for the manage account page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/?next=/account/" + content_type + "/")

    return render_to_response( "account.html",
        { "member" : member, "contentType" : content_type },
        context_instance = RequestContext(request) )


def reset_account_password_view(request):
    """Resets the logged in member's password."""
    # Get the member who is logged in (or raise a 404 error)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()
   
    # Create dictionaries to hold the POST data and the invalid errors
    data = { "current_password" : "", "new_password" : "", "confirm_new_password" : "" }
    invalid = { "errors" : [] }

    # Validate the POST data, if there is any
    if (request.POST):
        # Get the POST data
        try:
            data["current_password"] = request.POST["currentPassword"]
            data["new_password"] = request.POST["newPassword"]
            data["confirm_new_password"] = request.POST["confirmNewPassword"]
        except KeyError:
            pass

        # Validate the current password
        if (not data["current_password"]):
            invalid["current_password"] = True
            invalid["errors"].append("Current password not specified")

        elif (not member.check_password(data["current_password"])):
            invalid["current_password"] = True
            invalid["errors"].append("Current password is incorrect")

        # Validate the new password and confirm new password
        if ((not data["new_password"]) and (not data["confirm_new_password"])):
            invalid["new_password"] = True
            invalid["confirm_new_password"] = True
            data["new_password"] = ""
            data["confirm_new_password"] = ""
            invalid["errors"].append("New password not specified")
            invalid["errors"].append("Confirm new password not specified")

        elif (len(data["new_password"]) < 8):
            invalid["new_password"] = True
            invalid["confirm_new_password"] = True
            data["new_password"] = ""
            data["confirm_new_password"] = ""
            invalid["errors"].append("New password must contain at least eight characters")

        elif (data["new_password"] != data["confirm_new_password"]):
            invalid["new_password"] = True
            invalid["confirm_new_password"] = True
            data["new_password"] = ""
            data["confirm_new_password"] = ""
            invalid["errors"].append("New password and confirm new password do not match")
        
        # If all the POST data is valid, reset the logged in member's password
        if (not invalid["errors"]):
            member.set_password(data["new_password"])
            member.save()
            return HttpResponse()

    return render_to_response( "resetAccountPassword.html",
        { "data" : data, "invalid" : invalid },
        context_instance = RequestContext(request) )


def update_account_email_view(request):
    # Get the member who is logged in (or raise a 404 error)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    # Create dictionaries to hold the POST data and the invalid errors
    data = { "current_password" : "", "new_email" : "", "confirm_new_email" : "" }
    invalid = { "errors" : [] }

    # If there is POST data, validate it
    if (request.POST):
        # Get the POST data
        try:
            data["current_password"] = request.POST["currentPassword"]
            data["new_email"] = request.POST["newEmail"]
            data["confirm_new_email"] = request.POST["confirmNewEmail"]
        except KeyError:
            invalid_confirm_new_email = True
        
        # Validate the current password
        if (not data["current_password"]):
            invalid["current_password"] = True
            invalid["errors"].append("Current password not specified")

        elif (not member.check_password(data["current_password"])):
            invalid["current_password"] = True
            invalid["errors"].append("Current password is incorrect")

        # Validate the new email
        if (not data["new_email"]):
            invalid["new_email"] = True
            invalid["errors"].append("New email not specified")

        elif (not is_email(data["new_email"])):
            invalid["new_email"] = True
            invalid["errors"].append("Invalid new email format")

        elif (Member.objects.filter(username = data["new_email"])):
            invalid["new_email"] = True
            invalid["confirm_new_email"] = True
            invalid["errors"].append("An account already exists for the provided new email")

        elif (not ((data["new_email"].endswith("@nd.edu")) or (data["new_email"].endswith("@saintmarys.edu")) or (data["new_email"].endswith("@hcc-nd.edu")))):
            invalid["new_email"] = True
            invalid["confirm_new_email"] = True
            invalid["errors"].append("Inkle is currently limited to Notre Dame, Saint Mary's, and Holy Cross email addresses only")

        # Validate the confirm new email
        if (not data["confirm_new_email"]):
            invalid["confirm_new_email"] = True
            invalid["errors"].append("Confirm new email not specified")

        elif (not is_email(data["confirm_new_email"])):
            invalid["confirm_new_email"] = True
            invalid["errors"].append("Invalid confirm new email format")

        elif (data["new_email"] != data["confirm_new_email"]):
            invalid["new_email"] = True
            invalid["confirm_new_email"] = True
            invalid["errors"].append("New email and confirm new email do not match")

        # If all the POST data is valid, update the logged in member's email
        if (not invalid["errors"]):
            member.email = data["new_email"]
            member.username = data["new_email"]
            member.verified = False
            member.save()
            return HttpResponse()

    return render_to_response( "updateAccountEmail.html",
        { "data" : data, "invalid" : invalid },
        context_instance = RequestContext(request) )


def deactivate_account_view(request):
    # Get the member who is logged in (or raise a 404 error)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    # Create dictionaries to hold the POST data and the invalid errors
    data = { "password" : "" }
    invalid = { "errors" : [] }

    if (request.POST):
        # Get the POST data
        try:
            data["password"] = request.POST["password"]
        except KeyError:
            invalid_password = True

        # Validate the password
        if (not data["password"]):
            invalid["password"] = True
            invalid["errors"].append("Password not specified")

        elif (not member.check_password(data["password"])):
            invalid["password"] = True
            invalid["errors"].append("Password is incorrect")

        # If the password is correct, deactivate the logged in member's account
        if (not invalid["errors"]):
            # If the deactivate flag is set, deactivate the logged in member's account
            try:
                if (request.POST["deactivate"]):
                    member.is_active = False
                    member.save()
                    return HttpResponse()

            # Otherwise, do nothing
            except KeyError:
                return HttpResponse()

    return render_to_response( "deactivateAccount.html",
        { "data" : data, "invalid" : invalid },
        context_instance = RequestContext(request) )


def edit_profile_view(request, content_type = "information"):
    """Returns the HTML for the edit profile page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/?next=/editProfile/" + content_type + "/")

    return render_to_response( "editProfile.html",
        { "member" : member, "contentType" : content_type },
        context_instance = RequestContext(request) )


def edit_profile_information_view(request):
    """Updates the logged in member's profile information."""
    # Get the member who is logged in (or raise a 404 error)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    # Create dictionaries to hold the POST data and the invalid errors
    data = { "first_name" : member.first_name, "last_name" : member.last_name, "phone1" : member.phone[0:3], "phone2" : member.phone[3:6], "phone3" : member.phone[6:10], "street" : member.street, "city" : member.city, "state" : member.state, "zip_code" : member.zip_code, "month" : member.birthday.month, "day" : member.birthday.day, "year" : member.birthday.year, "gender" : member.gender }
    invalid = { "errors" : [] }

    if (request.POST):
        # Get the POST data
        try:
            data["first_name"] = request.POST["firstName"]
            data["last_name"] = request.POST["lastName"]
            data["phone1"] = request.POST["phone1"]
            data["phone2"] = request.POST["phone2"]
            data["phone3"] = request.POST["phone3"]
            data["street"] = request.POST["street"]
            data["city"] = request.POST["city"]
            data["state"] = request.POST["state"]
            data["zip_code"] = request.POST["zipCode"]
            data["month"] = request.POST["month"]
            data["day"] = request.POST["day"]
            data["year"] = request.POST["year"]
            data["gender"] = request.POST["gender"]
        except KeyError:
            pass

        # Validate the first name
        if (not data["first_name"]):
            invalid["first_name"] = True
            invalid["errors"].append("First name not specified")

        # Validate the last name
        if (not data["last_name"]):
            invalid["last_name"] = True
            invalid["errors"].append("Last name not specified")

        # Validate the phone number
        if (data["phone1"]):
            if (len(data["phone1"]) != 3):
                invalid["phone1"] = True
                invalid["errors"].append("Phone number section one must contain three digits")
            elif ([x for x in data["phone1"] if x not in "0123456789"]):
                invalid["phone1"] = True
                invalid["errors"].append("Phone number section one can only contain digits")

        if (data["phone2"]):
            if (len(data["phone2"]) != 3):
                invalid["phone2"] = True
                invalid["errors"].append("Phone number section two must contain three digits")
            elif ([x for x in data["phone2"] if x not in "0123456789"]):
                invalid["phone2"] = True
                invalid["errors"].append("Phone number section two can only contain digits")
        
        if (data["phone3"]):
            if (len(data["phone3"]) != 4):
                invalid["phone3"] = True
                invalid["errors"].append("Phone number section three must contain four digits")
            elif ([x for x in data["phone3"] if x not in "0123456789"]):
                invalid["phone3"] = True
                invalid["errors"].append("Phone number section three can only contain digits")

        if (data["phone1"] or data["phone2"] or data["phone3"]):
            if (not data["phone1"]):
                invalid["phone1"] = True
                invalid["errors"].append("Phone number section one not specified")
            if (not data["phone2"]):
                invalid["phone2"] = True
                invalid["errors"].append("Phone number section two not specified")
            if (not data["phone3"]):
                invalid["phone3"] = True
                invalid["errors"].append("Phone number section three not specified")

        # Validate the address
        if (data["street"] or data["city"] or data["state"] or data["zip_code"]):
            if (not data["city"]):
                invalid["city"] = True
                invalid["errors"].append("City not specified")
            if (not data["state"]):
                invalid["state"] = True
                invalid["errors"].append("State not specified")
            if (not data["zip_code"]):
                invalid["zip_code"] = True
                invalid["errors"].append("Zip code not specified")

        if (data["zip_code"]):
            if (len(data["zip_code"]) != 5):
                invalid["zip_code"] = True
                invalid["errors"].append("Zip code must contain five digits")
            elif ([x for x in data["zip_code"] if x not in "0123456789"]):
                invalid["zip_code"] = True
                invalid["errors"].append("Zip code can only contain digits")

        # Validate the birthday month
        if (not data["month"]):
            data["month"] = 0
            invalid["month"] = True
            invalid["errors"].append("Birthday month not specified")
        else:
            data["month"] = int(data["month"])

        # Validate the birthday day
        if (not data["day"]):
            data["day"] = 0
            invalid["day"] = True
            invalid["errors"].append("Birthday day not specified")
        else:
            data["day"] = int(data["day"])

        # Validate the birthday year
        if (not data["year"]):
            data["year"] = 0
            invalid["year"] = True
            invalid["errors"].append("Birthday year not specified")
        else:
            data["year"] = int(data["year"])

        # Validate the member is at least sixteen years old
        if (("month" not in invalid) and ("day" not in invalid) and ("year" not in invalid)):
            if (not is_sixteen(data["month"], data["day"], data["year"])):
                invalid["month"] = True
                invalid["day"] = True
                invalid["year"] = True
                invalid["errors"].append("You must be at least sixteen years old to use Inkle")

        # Validate the gender
        if (data["gender"] not in ["Male", "Female"]):
            invalid["gender"] = True
            invalid["errors"].append("Gender not specified")

        # If there are no errors, update the logged in member's profile information
        if (not invalid["errors"]):
            phone = data["phone1"] + data["phone2"] + data["phone3"]
            birthday = datetime.date(day = int(data["day"]), month = int(data["month"]), year = int(data["year"]))
            member.update_profile_information(data["first_name"], data["last_name"], phone, data["street"], data["city"], data["state"], data["zip_code"], birthday, data["gender"])
            member.save()
            return HttpResponse()

    return render_to_response( "editProfileInformation.html",
        { "data" : data, "invalid" : invalid },
        context_instance = RequestContext(request) )

def get_new_profile_picture_view(request):
    # Get the member who is logged in (or raise a 404 error)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()
    
    return render_to_response( "newProfilePicture.html",
        { "member" : member },
        context_instance = RequestContext(request) )



def edit_profile_picture_view(request):
    # Get the member who is logged in (or raise a 404 error)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    if (request.FILES):
        fileName = MEDIA_ROOT + "images/members/" + str(member.id) + ".jpg"
        destination = open(fileName, "wb+")
        for chunk in request.FILES["newProfilePicture"].chunks():
            destination.write(chunk)
        destination.close()
        member.changed_image += 1
        member.save()
        return render_to_response( "editProfilePicture.html",
            { "member" : member },
            context_instance = RequestContext(request) )
    else:
        if (request.POST):
            return HttpResponseRedirect("/editProfile/picture/")
        else:
            return render_to_response( "editProfilePicture.html",
                { "member" : member },
                context_instance = RequestContext(request) )


def edit_profile_privacy_view(request):
    # Get the member who is logged in (or raise a 404 error)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    try:
        location_privacy = int(request.POST["locationPrivacy"])
        email_privacy = int(request.POST["emailPrivacy"])
        phone_privacy = int(request.POST["phonePrivacy"])
        birthday_privacy = int(request.POST["birthdayPrivacy"])
        followers_privacy = int(request.POST["followersPrivacy"])
        following_privacy = int(request.POST["followingsPrivacy"])
        networks_privacy = int(request.POST["networksPrivacy"])
        place_privacy = int(request.POST["placePrivacy"])
        inklings_privacy = int(request.POST["inklingsPrivacy"])
    
        member.update_privacy_settings(location_privacy, email_privacy, phone_privacy, birthday_privacy, followers_privacy, following_privacy, networks_privacy, place_privacy, inklings_privacy)
        member.save()
    except KeyError:
        pass

    return render_to_response( "editProfilePrivacy.html",
        { "member" : member },
        context_instance = RequestContext(request) )


def edit_profile_email_preferences_view(request):
    # Get the member who is logged in (or raise a 404 error)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    try:
        requested_preference = (request.POST["requestedPreference"] == "true")
        accepted_preference = (request.POST["acceptedPreference"] == "true")
        invited_preference = (request.POST["invitedPreference"] == "true")
        general_preference = (request.POST["generalPreference"] == "true")

        member.update_email_preferences(requested_preference, accepted_preference, invited_preference, general_preference)
        member.save()
    except KeyError:
        pass

    return render_to_response( "editProfileEmailPreferences.html",
        { "member" : member },
        context_instance = RequestContext(request) )


def diagnostic_view(request):
    # Get the member who is logged in (or raise a 404 error)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()
    
    if (not member.is_staff):
        raise Http404()
    else:
        num_members = len(Member.objects.all())
        num_verified = len(Member.objects.filter(verified = True))
        num_unverified = num_members - num_verified
        return render_to_response( "diagnostic.html",
            { "member" : member, "num_members" : num_members, "num_verified" : num_verified, "num_unverified" : num_unverified },
            context_instance = RequestContext(request) )
        

def network_view(request, network_id = None):
    """Returns the HTML for the network page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        if (network_id):
            return HttpResponseRedirect("/login/?next=/network/" + network_id + "/")
        else:
            return HttpResponseRedirect("/login/")
    
    # Get the network corresponding to the inputted ID (or throw a 404 error if it is invalid)
    try:
        network = Network.objects.get(pk = network_id)
    except:
        raise Http404()

    # Get the network's members
    network.members = network.member_set.filter(is_active = True)
    network.num_members = len(network.members)

    # Determine the mutual following for each member in the network
    for m in network.members:
        m.mutual_followings = member.following.filter(is_active = True) & m.following.filter(is_active = True)
        m.privacy = get_privacy(member, m)

    if (member in network.members):
        network.button_list = [buttonDictionary["leave"]]
    else:
        network.button_list = [buttonDictionary["join"]]

    return render_to_response( "network.html",
        { "member" : member, "network" : network },
        context_instance = RequestContext(request) )


def terms_view(request):
    """Returns the HTML for the terms page."""
    # Get the member who is logged in (or set that member to None)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        member = None

    return render_to_response( "terms.html",
        { "member" : member },
        context_instance = RequestContext(request) )


def contact_view(request):
    """Returns the HTML for the contact page."""
    # Get the member who is logged in (or set that member to None)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        member = None

    # Create dictionaries to hold the POST data and the invalid errors
    if (member):
        data = { "name" : member.get_full_name(), "email" : member.email, "subject" : "", "message" : "" }
    else:
        data = { "name" : "", "email" : "", "subject" : "", "message" : "" }
    invalid = { "errors" : [] }

    if (request.POST):
        # Get the POST data
        try:
            data["name"] = request.POST["name"]
            data["email"] = request.POST["email"]
            data["subject"] = request.POST["subject"]
            data["message"] = request.POST["message"]
        except KeyError:
            pass

        # Validate the name
        if (not data["name"]):
            invalid["name"] = True
            invalid["errors"].append("Name not specified")

        # Validate the email
        if (not data["email"]):
            invalid["email"] = True
            invalid["errors"].append("Email not specified")

        elif (not is_email(data["email"])):
            invalid["email"] = True
            invalid["errors"].append("Invalid email format")

        # Validate the subject
        if (not data["subject"]):
            invalid["subject"] = True
            invalid["errors"].append("Subject not specified")

        # Validate the message
        if (not data["message"]):
            invalid["message"] = True
            invalid["errors"].append("Message not specified")
        
        return render_to_response( "contactForm.html",
            { "member" : member, "data" : data, "invalid" : invalid },
            context_instance = RequestContext(request) )

    return render_to_response( "contact.html",
        { "member" : member, "data" : data, "invalid" : invalid },
        context_instance = RequestContext(request) )


def location_view(request, location_id = None, content_type = "all", date = "today"):
    """Gets the members who are going to the inputted location today and returns the HTML for the location page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        if (location_id):
            return HttpResponseRedirect("/login/?next=/location/" + location_id + "/")
        else:
            return HttpResponseRedirect("/login/")
    
    # Get the location corresponding to the inputted ID (or throw a 404 error if it is invalid)
    try:
        location = Location.objects.get(pk = location_id)
    except:
        raise Http404()

    # Get date objects
    if date == "today":
        date1 = datetime.date.today()
    else:
        try:
            date1 = datetime.date(int(date.split("_")[2]), int(date.split("_")[0]), int(date.split("_")[1]) )
        except:
            date1 = datetime.date.today()
    dates = [date1 + datetime.timedelta(days = x) for x in range(3)]
    
    member = get_location_inklings(request.session["member_id"], location_id, None, date1)

    return render_to_response( "location.html",
        { "member" : member, "location" : location, "dates" : dates, "selectedDate" : date1, "content_type" : content_type },
        context_instance = RequestContext(request) )


def get_edit_location_html_view(request):
    """Returns the edit location HTML."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()
    
    # Make sure the logged in member can update the location
    if (not member.is_staff):
        raise Http404()
    
    # Get the location (or throw a 404 error if the location ID is invalid)
    try:
        location = Location.objects.get(pk = request.POST["locationID"])
    except:
        raise Http404()
  
    return render_to_response( "editLocationInfo.html",
        { "member" : member, "location" : location },
        context_instance = RequestContext(request) )


def get_search_content_view(request):
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        if "query" in request.POST:
            return HttpResponseRedirect("/login/?next=/search/" + request.POST["query"] + "/")
        else:
            return HttpResponseRedirect("/login/")
    
    if "query" in request.POST:
       # Strip the whitespace off the ends of the query
       query = request.POST["query"].strip()
    else:
        raise Http404()
    if "numDisplayed" in request.POST:
        numDisplayed = int(request.POST["numDisplayed"])
    else:
        numDisplayed = 0
    if ( ("contentType" not in request.POST) or (request.POST["contentType"] not in ["members", "locations", "networks"]) ):
        if "query" in request.POST:
            return HttpResponseRedirect("/login/?next=/search/" + request.POST["query"] + "/")
        else:
            return HttpResponseRedirect("/login/")
    elif request.POST["contentType"] == "members":
        # Get the members who match the search query
        members = members_search_query(query, Member.active.all(), numDisplayed)

        # Initialize member variables
        member.num_following = 0
        member.num_followers = 0
        member.num_other_people = 0

        # Determine each member's people type and button list
        for m in members:
            # Case 1: The logged in member is following and is being followed by the current member
            if ((m in member.following.filter(is_active = True)) and (member in m.following.filter(is_active = True))):
                m.people_type = "following follower"
                member.num_following += 1
                member.num_followers += 1
                m.show_contact_info = True
                #m.button_list = [buttonDictionary["prevent"], buttonDictionary["stop"], buttonDictionary["blots"]]
                m.button_list = [buttonDictionary["blots"]]

            # Case 2: The logged member is following the current member
            elif (m in member.following.filter(is_active = True)):
                m.people_type = "following"
                member.num_following += 1
                m.show_contact_info = True
                #m.button_list = [buttonDictionary["stop"], buttonDictionary["blots"]]
                m.button_list = [buttonDictionary["blots"]]

            # Case 3: The logged member is being followed by the current member
            elif (member in m.following.filter(is_active = True)):
                m.people_type = "follower"
                member.num_followers += 1
                m.show_contact_info = False
                if (m in member.pending.all()):
                    #m.button_list = [buttonDictionary["prevent"], buttonDictionary["revoke"]]
                    m.button_list = [buttonDictionary["revoke"]]
                else:
                    #m.button_list = [buttonDictionary["prevent"], buttonDictionary["request"]]
                    m.button_list = [buttonDictionary["request"]]

            # Case 4: Neither the logged in member nor the current member are following each other
            else:
                m.people_type = "other"
                member.num_other_people += 1
                m.show_contact_info = False
                if (m in member.pending.all()):
                    m.button_list = [buttonDictionary["revoke"]]
                else:
                    m.button_list = [buttonDictionary["request"]]

            # Determine the members who are being followed by both the logged in member and the current member
            m.mutual_followings = member.following.filter(is_active = True) & m.following.filter(is_active = True)
        
        return render_to_response( "searchMembers.html",
            {"member" : member, "members" : members},
            context_instance = RequestContext(request) )
            
    elif request.POST["contentType"] == "locations":
        # Get the locations which match the search query
        locations = locations_search_query(query, numDisplayed)
        
        return render_to_response( "searchLocations.html",
            {"locations" : locations},
            context_instance = RequestContext(request) )
        
    elif request.POST["contentType"] == "networks": 
        # Get the networks which match the search query
        networks = networks_search_query(query, numDisplayed)

        # Initialize member variables
        member.num_my_networks = 0
        member.num_other_networks = 0

        # Determine which networks the logged in member has joined and set their button lists accordingly
        for network in networks:
            if (network in member.networks.all()):
                network.network_type = "myNetworks"
                member.num_my_networks += 1
                network.button_list = [buttonDictionary["leave"]]
            else:
                network.network_type = "otherNetworks"
                member.num_other_networks += 1
                network.button_list = [buttonDictionary["join"]]

            # Determine the number of members in the current network
            network.num_members = len(network.member_set.filter(is_active = True))
        
        return render_to_response( "searchNetworks.html",
            {"networks" : networks},
            context_instance = RequestContext(request) )

def members_search_query(query, members, queryIndex = "all"):
    """Returns the members who match the inputted query."""
    # Split the query into words
    query_split = query.split()

    # If the query is only one word long, match the members' first or last names alone
    if (len(query_split) == 1):
        members = members.filter(Q(first_name__istartswith = query) | Q(last_name__istartswith = query))

    # If the query is two words long, match the members' first and last names
    elif (len(query_split) == 2):
        members = members.filter((Q(first_name__istartswith = query_split[0]) & Q(last_name__istartswith = query_split[1])) | (Q(first_name__istartswith = query_split[1]) & Q(last_name__istartswith = query_split[0])))

    # if the query is more than two words long, return no results
    else:
        members = []

    if queryIndex == "all":
        return members
    elif len(members) <= queryIndex: #If the number of members is <= the number of members already displayed, return nothing
        return []
    else:
        i = 0
        returnList = []
        while (i < 5 and (queryIndex + i) < len(members)):
            returnList.append(members[(queryIndex + i)])
            i += 1
        return returnList   

def locations_search_query(query, queryIndex = "all"):
    """Returns the locations which match the inputted query."""
    locations = Location.objects.filter(Q(name__icontains = query))
    if queryIndex == "all":
        return locations
    elif len(locations) <= queryIndex: #If the number of members is <= the number of members already displayed, return nothing
        return []
    else:
        i = 0
        returnList = []
        while (i < 5 and (queryIndex + i) < len(locations)):
            returnList.append(locations[(queryIndex + i)])
            i += 1
        return returnList
        

def networks_search_query(query, queryIndex = "all"):
    """Returns the networks which match the inputted query."""
    networks = Network.objects.filter(Q(name__icontains = query))
    if queryIndex == "all":
        return networks
    elif len(networks) <= queryIndex: #If the number of members is <= the number of members already displayed, return nothing
        return []
    else:
        i = 0
        returnList = []
        while (i < 5 and (queryIndex + i) < len(networks)):
            returnList.append( networks[(queryIndex + i)])
            i += 1
        return returnList

def blots_search_query(query, member):
    """Returns the blots which match the inputted query."""
    blots = member.blots.filter(Q(name__icontains = query))
    return blots


def search_view(request, query = ""):
    """Gets the members, locations, and networks which match the inputted query and returns the HTML for the search page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        if (query):
            return HttpResponseRedirect("/login/?next=/search/" + query + "/")
        else:
            return HttpResponseRedirect("/login/")
    
    # Strip the whitespace off the ends of the query
    query = query.strip()

    # Get the members who match the search query
    members = members_search_query(query, Member.active.all(), "all")

    # Initialize member variables
    member.num_following = 0
    member.num_followers = 0
    member.num_other_people = 0
    numMembers = len(members)

    # Determine each member's people type and button list
    for m in members:
        # Case 1: The logged in member is following and is being followed by the current member
        if ((m in member.following.filter(is_active = True)) and (member in m.following.filter(is_active = True))):
            m.people_type = "following follower"
            member.num_following += 1
            member.num_followers += 1
            m.show_contact_info = True
            #m.button_list = [buttonDictionary["prevent"], buttonDictionary["stop"], buttonDictionary["blots"]]
            m.button_list = [buttonDictionary["blots"]]

        # Case 2: The logged member is following the current member
        elif (m in member.following.filter(is_active = True)):
            m.people_type = "following"
            member.num_following += 1
            m.show_contact_info = True
            #m.button_list = [buttonDictionary["stop"], buttonDictionary["blots"]]
            m.button_list = [buttonDictionary["blots"]]

        # Case 3: The logged member is being followed by the current member
        elif (member in m.following.filter(is_active = True)):
            m.people_type = "follower"
            member.num_followers += 1
            m.show_contact_info = False
            if (m in member.pending.all()):
                #m.button_list = [buttonDictionary["prevent"], buttonDictionary["revoke"]]
                m.button_list = [buttonDictionary["revoke"]]
            else:
                #m.button_list = [buttonDictionary["prevent"], buttonDictionary["request"]]
                m.button_list = [buttonDictionary["request"]]

        # Case 4: Neither the logged in member nor the current member are following each other
        else:
            m.people_type = "other"
            member.num_other_people += 1
            m.show_contact_info = False
            if (m in member.pending.all()):
                m.button_list = [buttonDictionary["revoke"]]
            else:
                m.button_list = [buttonDictionary["request"]]

        # Determine the members who are being followed by both the logged in member and the current member
        m.mutual_followings = member.following.filter(is_active = True) & m.following.filter(is_active = True)
            
        # Determine the privacy rating for the logged in member and the current member
        m.privacy = get_privacy(member, m)

    # Get the locations which match the search query
    locations = locations_search_query(query, "all")
    numLocations = len(locations)
    
    # Get the networks which match the search query
    networks = networks_search_query(query, "all")
    numNetworks = len(networks)
    
    # Initialize member variables
    member.num_my_networks = 0
    member.num_other_networks = 0

    # Determine which networks the logged in member has joined and set their button lists accordingly
    for network in networks:
        if (network in member.networks.all()):
            network.network_type = "myNetworks"
            member.num_my_networks += 1
            network.button_list = [buttonDictionary["leave"]]
        else:
            network.network_type = "otherNetworks"
            member.num_other_networks += 1
            network.button_list = [buttonDictionary["join"]]

        # Determine the number of members in the current network
        network.num_members = len(network.member_set.filter(is_active = True))

    return render_to_response( "search.html",
        {"member" : member, "query" : query, "members" : members[0:5], "numMembers" : numMembers, "locations" : locations[0:5], "numLocations" : numLocations, "networks" : networks[0:5], "numNetworks" : numNetworks},
        context_instance = RequestContext(request) )


def suggestions_view(request):
    """Returns suggestions for the inputted query."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")
    
    # Get the POST data
    query = request.POST["query"].strip()
    query_type = request.POST["type"]

    # Initialize the list of suggestion categories
    categories = []
    
    # Case 1: Location suggestions for an inkling
    if (query_type == "inkling"):
        # Get the location suggestions (and add them to the categories list if there are any)
        locations = locations_search_query(query)[0:5]
        member_place = members_search_query(query, Member.active.filter(pk = request.session["member_id"]))
        if (member_place):
            member_place.suggestionType = "members"
            categories.append((member_place,))
        if (locations):
            locations.suggestionType = "locations"
            categories.append((locations,))
      
        # Set the number of characters to show for each suggestion
        num_chars = 23

        return render_to_response( "inklingSuggestions.html",
            { "member" : member, "categories" : categories, "queryType" : query_type, "numChars" : num_chars },
            context_instance = RequestContext(request) )
       
    # Case 2: Member, location, and network suggestions for the main header search
    elif (query_type == "search"):
        # Get the member suggestions (and add them to the categories list if there are any)
        members = members_search_query(query, Member.active.all())[0:3]
        if (members):
            members.suggestionType = "members"
            for m in members:
                m.name = m.first_name + " " + m.last_name
            categories.append((members, "People"))
        
        # Get the location suggestions (and add them to the categories list if there are any)
        locations = locations_search_query(query)[0:3]
        if (locations):
            locations.suggestionType = "locations"
            categories.append((locations, "Locations"))

        # Get the network suggestions (and add them to the categories list if there are any)
        networks = networks_search_query(query)[0:3]
        if (networks):
            networks.suggestionType = "networks"
            categories.append((networks, "Networks"))

        # Set the number of characters to show for each suggestion
        num_chars = 45

    # Case 3: Member suggestions for adding members to blots
    elif (query_type == "addToBlot"):
        # Get the requested blot (or throw a 404 error if the blot ID is invalid)
        try:
            blot = Blot.objects.get(pk = request.POST["blotID"])
        except:
            raise Http404()
            
        # Get the members who match the search query and who are not already in the requested blot (and add them to the categories list if there are any)
        members = members_search_query(query, member.following.all())
        members = members.exclude(pk__in = blot.members.all())[0:5]
        if (members):
            members.suggestionType = "members"
            for m in members:
                m.name = m.first_name + " " + m.last_name
            categories.append((members,))

        # Set the number of characters to show for each suggestion
        num_chars = 20

    # Case 4: Member and blot suggestions for inkling invites
    elif (query_type == "inklingInvite"):
        # Get the member suggestions (and add them to the categories list if there are any)
        members = members_search_query(query, Member.objects.filter(Q(id__in = member.following.filter(is_active=True)) | Q(id__in = member.followers.filter(is_active = True))))[0:5]
        if (members):
            members.suggestionType = "members"
            for m in members:
                m.name = m.first_name + " " + m.last_name
            categories.append((members, "People"))

        # Get the blots suggestions (and add them to the categories list if there are any)
        blots = blots_search_query(query, member)[0:5]
        if (blots):
            blots.suggestionType = "blots"
            categories.append((blots, "Blots"))
        
        # Set the number of characters to show for each suggestion
        num_chars = 20

    return render_to_response( "suggestions.html",
        { "categories" : categories, "queryType" : query_type, "numChars" : num_chars },
        context_instance = RequestContext(request) )


def notifications_view(request):
    """Gets the logged in member's request and returns the HTML for the notifications page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/?next=/manage/notifications/")

    # Get the members who have requested to follow the logged in member
    requested_members = member.requested.all()

    # For each requested member, determine their networks, mutual followings, and button list and allow their contact info to be seen
    for m in requested_members:
        m.mutual_followings = member.following.filter(is_active = True) & m.following.filter(is_active = True)
        m.button_list = [buttonDictionary["reject"], buttonDictionary["accept"]]
        # Determine the privacy rating for the logged in member and the current member
        m.privacy = get_privacy(member, m)
        
    return render_to_response( "notifications.html",
        { "member" : member, "requestedMembers" : requested_members },
        context_instance = RequestContext(request) )


def followers_view(request):
    """Gets the logged in member's or other member's followers and returns the HTML for the followers page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        if "other_member_id" in request.POST:
            return HttpResponseRedirect("/login/?next=/member/" + request.POST["other_member_id"] + "/")
        else:
            return HttpResponseRedirect("/login/?next=/manage/followers/")
            
    # If we are viewing another member's page, get the members who are following them
    if "other_member_id" in request.POST:
        # Get the member whose page is being viewed (or throw a 404 error if their member ID is invalid)
        try:
            other_member = Member.active.get(pk = request.POST["other_member_id"])
        except Member.DoesNotExist:
            raise Http404()

        # Get the members who are following the member whose page we are on and set the appropriate page context and no followers text
        members = other_member.followers.filter(is_active = True)
        page_context = "otherFollowers"
        no_followers_text = other_member.first_name + " " + other_member.last_name

        # Determine the privacy rating for the logged in member and the current member whose page is being viewed
        other_member.privacy = get_privacy(member, other_member)

        if (other_member.privacy < other_member.followers_privacy):
            return render_to_response( "noPermission.html",
                {},
                context_instance = RequestContext(request) )

    # Otherwise, get the members who are following the logged in member and set the appropriate page context and no followers text
    else:
        members = member.followers.filter(is_active = True)
        other_member = None
        page_context = "myFollowers"
        no_followers_text = "you"

    # Get the necessary information for each member's member card
    for m in members:
        # Case 1: The logged in member is the current member (or we are on someone else's profile page)
        if ((m == member) or (other_member)):
            m.button_list = []
            m.show_contact_info = True

        # Case 2: The logged in member has a pending request to follow the current member
        elif (m in member.pending.all()):
            m.button_list = [buttonDictionary["prevent"], buttonDictionary["revoke"]]
            m.show_contact_info = False

        # Case 3: The logged in member is following the current member
        elif (m in member.following.filter(is_active = True)):
            m.button_list = [buttonDictionary["prevent"], buttonDictionary["blots"]]
            m.show_contact_info = True

        # Case 4: The logged in member is not following and has not requested to follow the current member
        else:
            m.button_list = [buttonDictionary["prevent"], buttonDictionary["request"]]
            m.show_contact_info = False
            
        # Determine the members who are being followed by both the logged in member and the current member
        m.mutual_followings = member.following.filter(is_active = True) & m.following.filter(is_active = True)

        # Determine the privacy rating for the logged in member and the current member whose page is being viewed
        m.privacy = get_privacy(member, m)

    return render_to_response( "followers.html",
        { "member" : member, "members" : members, "pageContext" : page_context, "noFollowersText" : no_followers_text },
        context_instance = RequestContext(request) )


def get_member_following_view(request):
    """Gets the logged in member's or other member's following and returns the HTML for the following page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        if (request.POST["other_member_id"]):
            return HttpResponseRedirect("/login/?next=/member/" + request.POST["other_member_id"] + "/")
        else:
            return HttpResponseRedirect("/login/")
    
    # Get the member whose page is being viewed (or throw a 404 error if their member ID is invalid)
    try:
        other_member = Member.active.get(pk = request.POST["other_member_id"])
    except Member.DoesNotExist:
        raise Http404()

    # Get the members whom the other member is following
    members = [m for m in other_member.following.filter(is_active = True)]

    # Get the necessary information for each member's member card
    for m in members:
        # Case 1: The logged in member is the current member
        if ((m == member) or (other_member)):
            m.button_list = []
            m.show_contact_info = True

        # Case 2: The logged in member has a pending request to follow the current member
        elif (m in member.pending.all()):
            m.button_list = [buttonDictionary["prevent"], buttonDictionary["revoke"]]
            m.show_contact_info = False

        # Case 3: The logged in member is following the current member
        elif (m in member.following.filter(is_active = True)):
            m.button_list = [buttonDictionary["prevent"], buttonDictionary["blots"]]
            m.show_contact_info = True

        # Case 4: The logged in member is not following and has not requested to follow the current member
        else:
            m.button_list = [buttonDictionary["prevent"], buttonDictionary["request"]]
            m.show_contact_info = False
            
        # Determine the members who are being followed by both the logged in member and the current member
        m.mutual_followings = member.following.filter(is_active = True) & m.following.filter(is_active = True)
        
        # Determine the privacy rating for the logged in member and the current member whose page is being viewed
        m.privacy = get_privacy(member, m)

    # Determine the privacy rating for the logged in member and the current member whose page is being viewed
    other_member.privacy = get_privacy(member, other_member)

    if (other_member.privacy < other_member.followers_privacy):
        return render_to_response( "noPermission.html",
            {},
            context_instance = RequestContext(request) )
    else:
        return render_to_response( "following.html",
            { "member" : member, "otherMember" : other_member, "members" : members },
            context_instance = RequestContext(request) )
    
def blots_view(request, blot_id = None):
    """Gets the logged in member's blots returns the HTML for the blots page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/?next=/manage/blots/")

    # If a blot ID is specified, get the members in that blot (otherwise, get the members in the logged in member's accepted blot)
    try:
        blot = Blot.objects.get(pk = blot_id)
        members = blot.members.filter(is_active = True)
    except Blot.DoesNotExist:
        blot = None
        members = member.accepted.filter(is_active = True)

    # Get the necessary information for each member's member card
    for m in members:
        # Show the logged in member's contact information
        m.show_contact_info = True

        # Show the "Stop following" and "Blots" buttons
        m.button_list = [buttonDictionary["stop"], buttonDictionary["blots"]]

        # Determine the members who are being followed by both the logged in member and the current member
        m.mutual_followings = member.following.filter(is_active = True) & m.following.filter(is_active = True)

        # Determine the privacy rating for the logged in member and the current member
        m.privacy = get_privacy(member, m)

    # If a blot ID is specified, return only the blot content (otherwise, return the entire HTML for the blots page)
    try:
        content = request.POST["content"]
        html = "blotContent.html"
    except KeyError:
        html = "blots.html"

    return render_to_response( html, 
        { "member" : member, "members" : members, "blot" : blot},
        context_instance = RequestContext(request) )


def networks_view(request):
    """Gets the logged in member's or other member's networks and returns the HTML for the network page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        if "other_member_id" in request.POST:
            return HttpResponseRedirect("/login/?next=/member/" + request.POST["other_member_id"] + "/")
        else:
            return HttpResponseRedirect("/login/?next=/manage/networks/")

    # If we are viewing another member's page, get the members who are following them
    if "other_member_id" in request.POST:
        # Get the member whose page is being viewed (or throw a 404 error if their member ID is invalid)
        
        try:
            other_member = Member.active.get(pk = request.POST["other_member_id"])
        except Member.DoesNotExist:
            raise Http404()
            
        # Get the other member's networks
        networks = other_member.networks.all()
        
        # Determine the number of members in the current network
        for network in networks:
            network.num_members = len(network.member_set.filter(is_active = True))
            
        # Specify the page context
        page_context = "member"
        
        # Specify the text if the other member is not in any networks
        no_networks_text = other_member.first_name + " " + other_member.last_name + " is"
        
        # Determine the privacy rating for the logged in member and the current member whose page is being viewed
        other_member.privacy = get_privacy(member, other_member)
            
        if (other_member.privacy < other_member.networks_privacy):
            return render_to_response( "noPermission.html",
                {},
                context_instance = RequestContext(request) )
    
    # Otherwise, if no member ID is inputted, get the networks corresponding to the logged in member
    else:
        # Get the logged in member's networks
        networks = member.networks.all()
        
        # Give each network the "Leave network" button
        for network in networks:
            network.button_list = [buttonDictionary["leave"]]
            
            # Determine the number of members in the current network
            network.num_members = len(network.member_set.filter(is_active = True))
            
        # Specify the page context
        page_context = "manage"
        
        # Specify the text if the logged in member is not in any networks
        no_networks_text = "You are"
        
    return render_to_response( "networks.html",
        { "networks" : networks, "pageContext" : page_context, "noNetworksText" : no_networks_text },
        context_instance = RequestContext(request) )


def get_others_inklings_view(request):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
           return HttpResponseRedirect("/login")
     
    # Get the logged in member
    member = Member.active.get(pk = request.session["member_id"])

    # Get the POST data
    try:
        date = request.POST["date"].split("/")
        people_type = request.POST["peopleType"]
        people_id = request.POST["peopleID"]
        inkling_type = request.POST["inklingType"]
        include_member = request.POST["includeMember"]
    except KeyError:
        raise Http404()

    # Get others' inklings
    locations = get_others_inklings(member, datetime.date(day = int(date[1]), month = int(date[0]), year = int(date[2])), people_type, people_id, inkling_type)

    if (include_member == "true"):
        return render_to_response( "othersInklings.html",
            { "member" : member, "locations" : locations },
            context_instance = RequestContext(request) )
    else:
        return render_to_response( "locationBoard.html",
            { "locations" : locations },
            context_instance = RequestContext(request) )


def get_others_inklings(member, date, people_type, people_id, inkling_type):
    if (people_type == "other"):
        people = member.following.filter(is_active = True)

    elif (people_type == "network"):
        network = Network.objects.get(pk = people_id)
        people = network.member_set.filter(is_active = True)
    
    elif (people_type == "blot"):
        blot = Blot.objects.get(pk = people_id)
        people = blot.members.filter(is_active = True)

    locations = []
    for p in people:
        inkling = p.inklings.filter(date = date, category = inkling_type)
        if (inkling):
            if inkling[0].location:
                location = inkling[0].location
                if (location in locations):
                    for l in locations:
                        if (l == location):
                            l.count += 1
                else:
                    location.count = 1
                    locations.append(location)
            elif ((inkling[0].member_place in member.following.filter(is_active = True)) or (inkling[0].member_place in member.followers.filter(is_active = True)) or (inkling[0].member_place == member)):
                member_place = inkling[0].member_place
                if (member_place in locations):
                    for l in locations:
                        if (l == member_place):
                            l.count += 1
                else:
                    member_place.count = 1
                    locations.append(member_place)
    
    locations.sort(key = lambda l:-l.count)

    return locations


def get_member_inklings_view(request):

    # Get the member who is logged in (or throw a 404 error if their member ID is invalid)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    # Get the member whose page is being viewed (or throw a 404 error if their member ID is invalid)
    try:
        other_member = Member.active.get(pk = request.POST["other_member_id"])
    except Member.DoesNotExist:
        raise Http404()

    try:
        date = request.POST["date"].split("/")
        date = datetime.date(int(date[2]), int(date[0]), int(date[1]) )
    except KeyError:
        raise Http404()

    # Determine the privacy rating for the logged in member and the current member whose page is being viewed
    other_member.privacy = get_privacy(member, other_member)

    inklings = {}
    if (other_member.privacy >= other_member.inklings_privacy):
        try:
            inklings["dinner"] = other_member.inklings.get(date = date, category = "dinner")
        except:
            pass
        try:
            inklings["pregame"] = other_member.inklings.get(date = date, category = "pregame")
        except:
            pass
        try:
            inklings["mainEvent"] = other_member.inklings.get(date = date, category = "mainEvent")
        except:
            pass

        # Get date objects
        dates = [date + datetime.timedelta(days = x) for x in range(3)]
        
        return render_to_response( "memberInklings.html",
            { "inklings" : inklings, "dates" : dates, "selectedDate" : date },
            context_instance = RequestContext(request) )
    else:
        return render_to_response( "noPermission.html",
            {},
            context_instance = RequestContext(request) )


def login_view(request):
    """Either logs in a member or returns the login errors."""
    # If a member is already logged in, redirect them to the home page
    if ("member_id" in request.session):
        return HttpResponseRedirect("/")

    # Create dictionaries to hold the POST data and the invalid errors
    data = { "email" : "", "password" : "", "month" : 0, "year" : 0 }
    invalid = { "errors" : [] }

    # Get the next location after the login is successful (or set it to the home page if it is not set)
    try:
        next_location = request.GET["next"]
    except:
        next_location = "/"

    # If POST data is present, validate the username and password combination
    if (request.POST):
        # Get the POST data
        try:
            data["email"] = request.POST["email"].lower()
            data["password"] = request.POST["password"]
        except KeyError:
            pass

        # Validate the email
        if (not data["email"]):
            invalid["email"] = True
            invalid["errors"].append("Email not specified")

        elif (not is_email(data["email"])):
            invalid["email"] = True
            invalid["errors"].append("Invalid email format")

        # Validate the password
        if (not data["password"]):
            invalid["password"] = True
            invalid["errors"].append("Password not specified")
            
        # If an email and password are provided, the member is verified and active, and their password is correct, log them in (or set the login as invalid)
        if (not invalid["errors"]):
            # Get the member according to the provided email
            try:
                member = Member.active.get(username = data["email"])
            except:
                member = []

            # Confirm the username and password combination
            if (member and (member.verified) and (member.is_active) and (member.check_password(data["password"]))):
                request.session["member_id"] = member.id
                member.last_login = datetime.datetime.now()
                member.save()
                return HttpResponseRedirect(next_location)
            
            # Otherwise, set the invalid dictionary
            else:
                invalid["email"] = True
                invalid["password"] = True
                invalid["errors"].append("Invalid email/password combination")

    return render_to_response( "login.html",
        {"selectedContentLink" : "login", "loginData" : data, "loginInvalid" : invalid, "next" : next_location },
        context_instance = RequestContext(request) )


def reset_password_view(request, email = None, verification_hash = None):
    """Verifies a member's email address using the inputted verification hash."""
    # Get the member corresponding to the provided email (or raise a 404 error)
    try:
        member = Member.active.get(username = email)
    except Member.DoesNotExist:
        raise Http404()

    # If the verification hash is correct update the member's verification and let them reset their password (otherwise, raise a 404 error)
    if (member.verification_hash == verification_hash):
        member.update_verification_hash()
        member.save()
    else:
        raise Http404()
        
    return render_to_response( "login.html",
        { "selectedContentLink" : "login", "loginContent" : "resetPassword", "m" : member },
        context_instance = RequestContext(request) )

def is_sixteen(month, day, year):
    """Returns true if the inputted date represents a birthday of someone who is at least sixteen; otherwise, returns False."""
    born = datetime.date(day = int(day), month = int(month), year = int(year))
    today = datetime.date.today()
    
    try:
        birthday = born.replace(year = today.year)
    except ValueError:
        birthday = born.replace(year = today.year, day = born.day - 1)
    
    if birthday > today:
        age = today.year - born.year - 1
    else:
        age = today.year - born.year

    if (age < 16):
        return False
    else:
        return True


def register_view(request):
    """User login."""
    # If a member is already logged in, redirect them to the home page
    if ("member_id" in request.session):
        return HttpResponseRedirect("/")
    
    # If no POST data is present, redirect the member to the login view
    if (not request.POST):
        return HttpResponseRedirect("/login/")
    
    # Create a new user and log them in if they provided valid form data
    else:
        # Create dictionaries to hold the POST data and the invalid errors
        data = { "first_name" : "", "last_name" : "", "email" : "", "confirm_email" : "", "password" : "", "confirm_password" : "", "month" : 0, "day" : 0, "year" : 0, "gender" : "" }
        invalid = { "errors" : [] }

        # Get the POST data
        try:
            data["first_name"] = request.POST["firstName"]
            data["last_name"] = request.POST["lastName"]
            data["email"] = request.POST["email"].lower()
            data["confirm_email"] = request.POST["confirmEmail"].lower()
            data["password"] = request.POST["password"]
            data["confirm_password"] = request.POST["confirmPassword"]
            data["month"] = int(request.POST["month"])
            data["day"] = int(request.POST["day"])
            data["year"] = int(request.POST["year"])
            data["gender"] = request.POST["gender"]
        except KeyError:
            pass

        # Validate the first name
        if (not data["first_name"]):
            invalid["first_name"] = True
            invalid["errors"].append("First name not specified")

        # Validate the last name
        if (not data["last_name"]):
            invalid["last_name"] = True
            invalid["errors"].append("Last name not specified")

        # Validate the email
        if (not data["email"]):
            invalid["email"] = True
            invalid["errors"].append("Email not specified")

        elif (not is_email(data["email"])):
            invalid["email"] = True
            invalid["errors"].append("Invalid email format")

        elif (Member.objects.filter(username = data["email"])):
            invalid["email"] = True
            invalid["confirm_email"] = True
            invalid["errors"].append("An account already exists for the provided email")

        # Validate the confirm email
        if (not data["confirm_email"]):
            invalid["confirm_email"] = True
            invalid["errors"].append("Confirm email not specified")

        elif (not is_email(data["confirm_email"])):
            invalid["confirm_email"] = True
            invalid["errors"].append("Invalid confirm email format")

        elif (data["email"] != data["confirm_email"]):
            invalid["email"] = True
            invalid["confirm_email"] = True
            invalid["errors"].append("Email and confirm email do not match")
            
        elif (not ((data["email"].endswith("@nd.edu")) or (data["email"].endswith("@saintmarys.edu")) or (data["email"].endswith("@hcc-nd.edu")))):
            invalid["email"] = True
            invalid["confirm_email"] = True
            invalid["errors"].append("Inkle is currently limited to Notre Dame, Saint Mary's, and Holy Cross email addresses only")
        
        #elif (data["email"] == "mrobert7@nd.edu"):
        #    invalid["email"] = True
        #    invalid["confirm_email"] = True
        #    invalid["errors"].append("Mason, you can't sign up for Inkle because we don't have enough space (i.e. jiggabytes) for you. Lose some weight and we'll see what we can do.")
            
        # Validate the password and confirm password
        if ((not data["password"]) and (not data["confirm_password"])):
            invalid["password"] = True
            invalid["confirm_password"] = True
            data["password"] = ""
            data["confirm_password"] = ""
            invalid["errors"].append("Password not specified")
            invalid["errors"].append("Confirm password not specified")

        elif (len(data["password"]) < 8):
            invalid["password"] = True
            invalid["confirm_password"] = True
            data["password"] = ""
            data["confirm_password"] = ""
            invalid["errors"].append("Password must contain at least eight characters")

        elif (data["password"] != data["confirm_password"]):
            invalid["password"] = True
            invalid["confirm_password"] = True
            data["password"] = ""
            data["confirm_password"] = ""
            invalid["errors"].append("Password and confirm password do not match")

        # Validate the birthday month
        if (not data["month"]):
            invalid["month"] = True
            invalid["errors"].append("Birthday month not specified")

        # Validate the birthday day
        if (not data["day"]):
            invalid["day"] = True
            invalid["errors"].append("Birthday day not specified")

        # Validate the birthday year
        if (not data["year"]):
            invalid["year"] = True
            invalid["errors"].append("Birthday year not specified")

        # Validate the member is at least sixteen years old
        if (("month" not in invalid) and ("day" not in invalid) and ("year" not in invalid)):
            if (not is_sixteen(data["month"], data["day"], data["year"])):
                invalid["month"] = True
                invalid["day"] = True
                invalid["year"] = True
                invalid["errors"].append("You must be at least sixteen years old to use Inkle")

        # Validate the gender
        if (data["gender"] not in ["Male", "Female"]):
            invalid["gender"] = True
            invalid["errors"].append("Gender not specified")

        # If the registration form is valid, create a new member with the provided POST data
        if (not invalid["errors"]):
            # Create the new member
            member = Member(
                first_name = data["first_name"],
                last_name = data["last_name"],
                username = data["email"],
                email = data["email"],
                birthday = datetime.date(day = data["day"], month = data["month"], year = data["year"]),
                gender = data["gender"]
            )
            
            # Set the new member's password
            member.set_password(data["password"])
        
            # Set the new member's verification hash
            member.update_verification_hash()

            # Save the new member
            member.save()

            # Create default image for the new member
            if (member.gender == "Male"):
                #shutil.copyfile("static/media/images/main/man.jpg", "static/media/images/members/" + str(member.id) + ".jpg")
                shutil.copyfile(MEDIA_ROOT + "images/main/man.jpg", MEDIA_ROOT + "images/members/" + str(member.id) + ".jpg")
            else:
                shutil.copyfile(MEDIA_ROOT + "images/main/woman.jpg", MEDIA_ROOT + "images/members/" + str(member.id) + ".jpg")

            # Send the member to the successful account creation page
            return render_to_response( "registrationConfirmation.html",
                { "email" : data["email"] },
                context_instance = RequestContext(request) )

    return render_to_response( "registrationForm.html",
        { "selectedContentLink" : "registration", "registrationData" : data, "registrationInvalid" : invalid },
        context_instance = RequestContext(request) )


def verify_email_view(request, email = None, verification_hash = None):
    """Verifies a member's email address using the inputted verification hash."""
    # Get the member corresponding to the provided email (otherwise, throw a 404 error)
    try:
        member = Member.active.get(username = email)
    except Member.DoesNotExist:
        raise Http404()

    # If the member has not yet been verified and the verification hash is correct, verify the member and give them a new verification hash (otherwise, throw a 404 error)
    if ((not member.verified) and (member.verification_hash == verification_hash)):
        member.update_verification_hash()
        member.verified = True
        member.save()
    else:
        raise Http404()

    return render_to_response( "login.html",
        { "selectedContentLink" : "registration", "registrationContent" : "verifyEmail", "m" : member },
        context_instance = RequestContext(request) )


def logout_view(request):
    """Logs out the logged in member."""
    try:
        del request.session["member_id"]
    except KeyError:
        pass

    return HttpResponseRedirect("/login/")

def getting_started_view(request):
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    return render_to_response( "gettingStarted.html",
        { "member" : member },
        context_instance = RequestContext(request) )

def help_view(request, content_type = "overview"):
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        member = None

    try:
        first_load = request.POST["firstLoad"]
        first_load = False
    except KeyError:
        first_load = True

    if (first_load):
        return render_to_response( "help.html",
            { "member" : member, "contentType" : content_type },
            context_instance = RequestContext(request) )
    else:
        return render_to_response( "help" + content_type[0].upper() + content_type[1:] + ".html",
            { "member" : member, "contentType" : content_type },
            context_instance = RequestContext(request) )
