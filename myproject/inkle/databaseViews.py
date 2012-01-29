from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.shortcuts import render_to_response

from django.contrib.auth.models import User
from django.contrib import auth

from myproject.inkle.models import *
from myproject.inkle.emails import *

import datetime
import shutil

buttonDictionary = {
    "request" : ("requestToFollow", "Request to follow", "Send a request to start following this person"),
    "prevent" : ("preventFollowing", "Block", "No longer allow this person to follow me"),
    "revoke" : ("revokeRequest", "Revoke request", "Revoke my request to follow this person"),
    "stop" : ("stopFollowing", "Stop following", "Stop following this person"),
    "circles" : ("circlesCardButton", "Circles"),
    "reject" : ("rejectRequest", "Reject request", "Do not allow this person to follow me"),
    "accept" : ("acceptRequest", "Accept request", "Allow this person to follow me"),
    "join" : ("joinSphere", "Join sphere", "Beome a member of this sphere"),
    "leave" : ("leaveSphere", "Leave sphere", "I no longer wish to be a part of this sphere"),
}

def date_selected_view(request):
    """Updates the calendar once a date is clicked."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except (Member.DoesNotExist, KeyError) as e:
        return HttpResponseRedirect("/login/")
    
    if request.POST["arrow"] == "today":
        date1 = datetime.date.today()
        selectedDate = date1
    elif request.POST["arrow"] == "left":
        date1 = datetime.date(int(request.POST["firstYear"]), int(request.POST["firstMonth"]), int(request.POST["firstDay"])) - datetime.timedelta(days = 1)
        selectedDate = datetime.date(int(request.POST["selectedYear"]), int(request.POST["selectedMonth"]), int(request.POST["selectedDay"]))
    elif request.POST["arrow"] == "right":
        date1 = datetime.date(int(request.POST["firstYear"]), int(request.POST["firstMonth"]), int(request.POST["firstDay"])) + datetime.timedelta(days = 1)
        selectedDate = datetime.date(int(request.POST["selectedYear"]), int(request.POST["selectedMonth"]), int(request.POST["selectedDay"]))
    
    dates = [date1 + datetime.timedelta(days = x) for x in range(int(request.POST["numDates"]))]
    
    return render_to_response( "calendar.html",
        {"dates" : dates, "selectedDate" : selectedDate },
        context_instance = RequestContext(request) )

def get_location_inklings_view(request):
    # Get the member who is logged in (or redirect them to the login page)
    print "---------------"
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        print "except"
        if (request.POST["location_id"]):
            return HttpResponseRedirect("/login/?next=/location/" + request.POST["location_id"] + "/")
        else:
            return HttpResponseRedirect("/login/")

    print "dateObjects"
    # Get date objects
    date1 = datetime.date(int(request.POST["year"]), int(request.POST["month"]), int(request.POST["day"]))
    dates = [date1 + datetime.timedelta(days = x) for x in range(3)]

    print "member call"
    member = get_location_inklings(request.session["member_id"], request.POST["location_id"], date1)
    print "member return"
    
    return render_to_response( "locationInklings.html",
        { "member" : member},
        context_instance = RequestContext(request) )

def get_location_inklings(member_id = None, location_id = None, date = datetime.date.today()):
    """Returns a member object with additional fields indicating inklings at the input location for the input datetime date object"""

    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.active.get(pk = member_id)
    except:
        if (location_id):
            return HttpResponseRedirect("/login/?next=/location/" + location_id + "/")
        else:
            return HttpResponseRedirect("/login/")
    # Get the location corresponding to the inputted ID (or throw a 404 error if it is invalid)
    try:
        location = Location.objects.get(pk = int(location_id))
    except:
        raise Http404()
    
    # Get the people whom the logged in member is following
    following = member.following.filter(is_active = True)

    # Get all of the specified date's inklings at the provided location
    dateReformat = str(date.month) + "/" + str(date.day) + "/" + str(date.year)
    location_inklings = Inkling.objects.filter(date = dateReformat, location = location)

    # Get the logged in member's dinner inkling and the members who are attending
    try:
        dinner_inkling = location_inklings.get(category = "dinner")
        all_dinner_members = dinner_inkling.member_set.all()
        member.dinner_members = [m for m in all_dinner_members if (m in following)]
        member.num_dinner_others = len(all_dinner_members) - len(member.dinner_members)
        for m in member.dinner_members:
            m.show_contact_info = True
            m.mutual_followings = member.following.filter(is_active = True) & m.following.filter(is_active = True)
            m.button_list = [buttonDictionary["circles"]]
    except Inkling.DoesNotExist:
        member.dinner_members = []
        member.num_dinner_others = 0

    # Get the logged in member's pregame inkling and the members who are attending
    try:
        pregame_inkling = location_inklings.get(category = "pregame")
        all_pregame_members = pregame_inkling.member_set.all()
        member.pregame_members = [m for m in all_pregame_members if (m in following)]
        member.num_pregame_others = len(all_pregame_members) - len(member.pregame_members)
        for m in member.pregame_members:
            m.show_contact_info = True
            m.mutual_followings = member.following.filter(is_active = True) & m.following.filter(is_active = True)
            m.button_list = [buttonDictionary["circles"]]
    except Inkling.DoesNotExist:
        member.pregame_members = []
        member.num_pregame_others = 0

    # Get the logged in member's main event inkling and the members who are attending
    try:
        main_event_inkling = location_inklings.get(category = "mainEvent")
        all_main_event_members = main_event_inkling.member_set.all()
        member.main_event_members = [m for m in all_main_event_members if (m in following)]
        member.num_main_event_others = len(all_main_event_members) - len(member.main_event_members)
        for m in member.main_event_members:
            m.show_contact_info = True
            m.mutual_followings = member.following.filter(is_active = True) & m.following.filter(is_active = True)
            m.button_list = [buttonDictionary["circles"]]
    except Inkling.DoesNotExist:
        member.main_event_members = []
        member.num_main_event_others = 0
        
    return member 

def edit_location_view(request):
    """Edits a location's Location object."""
    # Get the member who is logged in (or raise a 404 error if the member ID is invalid)
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
   
    try:
        # Update the location's information using the POST data
        location.name = request.POST["name"]
        location.street = request.POST["street"]
        location.city = request.POST["city"]
        location.state = request.POST["state"]
        location.zip_code = int(request.POST["zipCode"])
        location.phone = request.POST["phone"]
        location.category = request.POST["category"]
        location.website = request.POST["website"]
        location.image = request.POST["image"]

        # Make sure the location begins with "http://www."
        if (location.website):
            if ((not location.website.startswith("http://")) and (not location.website.startswith("www"))):
                location.website = "http://www." + location.website
            elif (not location.website.startswith("http://")):
                location.website = "http://" + location.website
    
        # Save the location's updated information
        location.save()

    except KeyError:
        pass

    return render_to_response( "locationInfo.html",
        {"member" : member, "location" : location},
        context_instance = RequestContext(request) )


def request_to_follow_view(request):
    """Sends a request from the from_member to follow the to_member."""
    # Get the member who sent the request (or raise a 404 error if the member ID is invalid)
    try:
        from_member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    # Get the member to whom the request is being sent (or raise a 404 error if the member ID is invalid)
    try:
        to_member = Member.active.get(pk = request.POST["toMemberID"])
    except:
        raise Http404()

    # Update the database to signify the request
    from_member.pending.add(to_member)
    to_member.requested.add(from_member)

    # Return the updated tooltip
    return HttpResponse(buttonDictionary["revoke"][2])


def revoke_request_view(request):
    """Revokes the request from the from_member to follow the to_member."""
    # Get the member who sent the request (or raise a 404 error if the member ID is invalid)
    try:
        from_member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    # Get the member to whom the request is being sent (or raise a 404 error if the member ID is invalid)
    try:
        to_member = Member.active.get(pk = request.POST["toMemberID"])
    except:
        raise Http404()

    # Update the database to signify the revoking of the request
    from_member.pending.remove(to_member)
    to_member.requested.remove(from_member)

    return render_to_response( "revokeRequestConfirmation.html",
        { "member" : to_member },
        context_instance = RequestContext(request) )


def accept_request_view(request):
    """Accepts the request from the from_member to follow the to_member."""
    # Get the member to whom the request is being sent (or raise a 404 error if the member ID is invalid)
    try:
        to_member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    # Get the member who sent the request (or raise a 404 error if the member ID is invalid)
    try:
        from_member = Member.active.get(pk = request.POST["fromMemberID"])
    except:
        raise Http404()

    # Update the database to signify the accepted request
    from_member.pending.remove(to_member)
    to_member.requested.remove(from_member)
    to_member.followers.add(from_member)
    from_member.following.add(to_member)
    from_member.accepted.add(to_member)
    
    return render_to_response( "requestConfirmation.html",
        { "member" : from_member, "acceptedOrRejected" : "accepted" },
        context_instance = RequestContext(request) )


def reject_request_view(request):
    """Rejects the request from the from_member to follow the to_member."""
    # Get the member to whom the request is being sent (or raise a 404 error if the member ID is invalid)
    try:
        to_member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    # Get the member who sent the request (or raise a 404 error if the member ID is invalid)
    try:
        from_member = Member.active.get(pk = request.POST["fromMemberID"])
    except:
        raise Http404()

    # Update the database to signify the request
    from_member.pending.remove(to_member)
    to_member.requested.remove(from_member)

    return render_to_response( "requestConfirmation.html",
        { "member" : from_member, "acceptedOrRejected" : "rejected" },
        context_instance = RequestContext(request) )


def stop_following_view(request):
    """Makes the from_member stop following the to_member."""
    # Get the member who sent the request (or raise a 404 error if the member ID is invalid)
    try:
        from_member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    # Get the member to whom the request was sent (or raise a 404 error if the member ID is invalid)
    try:
        to_member = Member.active.get(pk = request.POST["toMemberID"])
    except:
        raise Http404()

    # Make the from_member stop following the to_member
    remove_following(from_member, to_member)

    return HttpResponse()


def prevent_following_view(request):
    """Makes the from_member stop following the to_member."""
    # Get the member to whom the request was sent (or raise a 404 error if the member ID is invalid)
    try:
        to_member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    # Get the member who sent the request (or raise a 404 error if the member ID is invalid)
    try:
        from_member = Member.active.get(pk = request.POST["fromMemberID"])
    except:
        raise Http404()

    # Make the from_member stop following the to_member
    remove_following(from_member, to_member)

    return render_to_response( "preventFollowingConfirmation.html",
        { "member" : from_member },
        context_instance = RequestContext(request) )


def remove_following(from_member, to_member):
    """Makes the from_member stop following the to_member."""
    # Remove the to_member from the from_member's accepted list
    from_member.accepted.remove(to_member)

    # Remove the to_member from all of the from_member's circles
    for circle in from_member.circles.all():
        circle.members.remove(to_member)

    # Remove the from_member follower of to_member
    to_member.followers.remove(from_member)
    
    # Remove to_member from from_member's following list
    from_member.following.remove(to_member)

    return


def add_to_circle_view(request):
    """Adds the to_member to one of from_member's circles."""
    # Get the member who sent the request (or raise a 404 error if the member ID is invalid)
    try:
        from_member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    # Get the member to whom the request was sent (or raise a 404 error if the member ID is invalid)
    try:
        to_member = Member.active.get(pk = request.POST["toMemberID"])
    except:
        raise Http404()

    # Get the circle to which to_member is being added (or raise a 404 error if the circle ID is invalid)
    try:
        circle = Circle.objects.get(pk = request.POST["circleID"])
    except:
        raise Http404()

    # Add the to_member to the circle
    circle.members.add(to_member)

    # If the to_member was only in the accepted list, remove them from the accepted list
    if (to_member in from_member.accepted.all()):
        from_member.accepted.remove(to_member)
    
    # Get the to_member's info for their member card
    to_member.mutual_followings = from_member.following.filter(is_active = True) & to_member.following.filter(is_active = True)
    to_member.button_list = [buttonDictionary["stop"], buttonDictionary["circles"]]
    to_member.show_contact_info = True
   
    return render_to_response( "memberCard.html",
        { "m" : to_member },
        context_instance = RequestContext(request) )


def remove_from_circle_view(request):
    """Removes the to_member from one of from_member's circles."""
    # Get the member who sent the request (or redirect them to the login page)
    try:
        from_member = Member.active.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")

    # Get the member to whom the request was sent (or throw a 404 error if the to member ID is invalid)
    try:
        to_member = Member.active.get(pk = request.POST["toMemberID"])
    except:
        raise Http404()
    
    # Get the circle to which to_member is being removed (or raise a 404 error if the circle ID is invalid)
    try:
        circle = Circle.objects.get(pk = request.POST["circleID"])
    except:
        raise Http404()

    # Remove the to_member from the from_member's circle
    remove_from_circle(from_member, to_member, circle)

    return HttpResponse()


def remove_from_circle(from_member, to_member, circle):
    """Removes the to_member from one of from_member's circles."""
    # Remove the to_member from the from_member's circle
    circle.members.remove(to_member)

    # Get the number of from_member's circles which to_member is in
    count = len([c for c in from_member.circles.all().select_related("members") if (to_member in c.members.filter(is_active = True))])

    # Add the to_member to the from_member's accepted list if the to_member no longer belongs to any of from_member's circles
    if (count == 0):
        from_member.accepted.add(to_member)

    return


def create_circle_view(request):
    """Create a new circle for the logged in member."""
    # Get the logged in member (or raise a 404 error if the member ID is invalid)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    # Create the new circle and add it to the logged in member's circles list
    circle = Circle.objects.create(name = request.POST["circleName"])
    member.circles.add(circle)

    # Return the new circle's ID
    return HttpResponse(circle.id)


def rename_circle_view(request):
    """Updates the name of one of the logged in member's circles."""
    # Get the logged in member (or raise a 404 error if the member ID is invalid)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    # Update the requested circle's name (or raise a 404 error if the circle ID is invalid)
    try:
        circle = member.circles.filter(pk = request.POST["circleID"]).update(name = request.POST["circleName"])
    except KeyError:
        raise Http404()

    return HttpResponse()


def delete_circle_view(request):
    """Deletes one of the logged in member's circles."""
    # Get the logged in member (or raise a 404 error if the member ID is invalid)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    # Get the circle which is to be deleted (or raise a 404 error if the circle ID is invalid)
    try:
        circle = Circle.objects.get(pk = request.POST["circleID"])
    except:
        raise Http404()

    # Remove each member from the circle to be deleted 
    for m in circle.members.all():
        remove_from_circle(member, m, circle)

    # Remove the circle to be deleted from the logged in member's circles list
    member.circles.remove(circle)
    
    # Delete the circle
    circle.delete()

    return HttpResponse()


def join_sphere_view(request):
    """Makes the logged in member join a sphere."""
    # Get the logged in member (or raise a 404 error if the member ID is invalid)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    # Get the sphere which is being joined (or raise a 404 error if the sphere ID is invalid)
    try:
        sphere = Sphere.objects.get(pk = request.POST["sphereID"])
    except:
        raise Http404()

    # Add the sphere to the logged in member's spheres list
    member.spheres.add(sphere)

    return HttpResponse()


def leave_sphere_view(request):
    """Makes the logged in member leave a sphere."""
    # Get the logged in member (or raise a 404 error if the member ID is invalid)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    # Get the sphere which is being left (or raise a 404 error if the sphere ID is invalid)
    try:
        sphere = Sphere.objects.get(pk = request.POST["sphereID"])
    except:
        raise Http404()

    # Remove the sphere from the logged in member's spheres list
    member.spheres.remove(sphere)

    return HttpResponse()


def create_inkling_view(request):
    """Adds an inkling to the logged in member's inklings."""
    # Get the logged in member (or raise a 404 error if the member ID is invalid)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()
   
    # Get the POST data
    inkling_type = request.POST["inklingType"]
    location = Location.objects.get(pk = request.POST["locationID"])
    date = request.POST["date"]

    # Get the inkling for the location/type/date combination (or create it if no inkling exists)
    try:
        inkling = Inkling.objects.get(location = location, category = inkling_type, date = date)
    except Inkling.DoesNotExist:
        inkling = Inkling(location = location, category = inkling_type, date = date)
        inkling.save()
    
    # See if the logged in member already has an inkling for the location/date combination
    try:
        conflicting_inkling = member.inklings.get(category = inkling_type, date = date)
        if (conflicting_inkling != inkling):
            remove_inkling(member, conflicting_inkling)
    except Inkling.DoesNotExist:
        pass

    # Add the inkling to the logged in member's inklings list
    member.inklings.add(inkling)

    # Return the location's name and image
    return HttpResponse(location.name + "|<|>|" + str(location.id))


def remove_inkling_view(request):
    """Removes an inkling from the logged in member's inklings."""
    # Get the logged in member (or raise a 404 error if the member ID is invalid)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()
    
    # Get the POST data
    inkling_type = request.POST["inklingType"]
    date = request.POST["date"]
    
    # Get the inkling for the member/type/date combination and remove it if possible
    try:
        inkling = member.inklings.get(category = inkling_type, date = date)
        remove_inkling(member, inkling)
    except Inkling.DoesNotExist:
        pass

    return HttpResponse()


def remove_inkling(member, inkling):
    """Removes and inkling from the member's inklings."""
    # Remove the inkling from the member's inkling list
    member.inklings.remove(inkling)

    # If the inkling no longer has any attendees, delete it
    if (not inkling.member_set.all()):
        inkling.delete()

    return


def get_my_inklings_view(request):
    """Returns the logged in member's inklings for the inputted date."""
    # Get the logged in member (or raise a 404 error if the member ID is invalid)
    try:
        member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()
    
    # Get the POST data
    date = request.POST["date"]
    
    #Get the date to be viewed
    month = int(request.POST["date"].split('/')[0])
    day = int(request.POST["date"].split('/')[1])
    year = int(request.POST["date"].split('/')[2])
    viewDate = datetime.date(year, month, day)
    
    pastDate = False
    if viewDate < datetime.date.today():
        pastDate = True
    
    # Get the names and images for the logged in member's inkling locations
    member.dinner_location, member.pregame_location, member.main_event_location = get_inklings(member, date)

    return render_to_response( "myInklings.html",
        { "member" : member, "pastDate" : pastDate },
        context_instance = RequestContext(request) )


def get_inklings(member, date):
    """Returns the names and images for the logged in member's inkling locations."""
    # Get the name and image for the logged in member's dinner inkling location
    try:
        inkling = member.inklings.get(date = date, category = "dinner")
        dinner_location = inkling.location
    except Inkling.DoesNotExist:
        dinner_location = None
    
    # Get the name and image for the logged in member's pregame inkling location
    try:
        inkling = member.inklings.get(date = date, category = "pregame")
        pregame_location = inkling.location
    except Inkling.DoesNotExist:
        pregame_location = None

    # Get the name and image for the logged in member's main event inkling location
    try:
        inkling =  member.inklings.get(date = date, category = "mainEvent")
        main_event_location = inkling.location
    except Inkling.DoesNotExist:
        main_event_location = None

    # Return the dinner, pregame, and main event locations
    return (dinner_location, pregame_location, main_event_location)


def create_sphere_view(request):
    """Creates a new Sphere object."""
    # Create a new sphere using the POST data and save it
    sphere = Sphere(name = request.POST["sphereName"])
    sphere.save()

    # Copy the default sphere image
    shutil.copyfile("static/media/images/main/sphere.jpg", "static/media/images/spheres/" + str(sphere.id) + ".jpg")

    return HttpResponse()
    

def create_location_view(request):
    """Creates a new Location object."""
    # Create a new location using the POST data and save it
    location = Location(
        name = request.POST["locationName"],
        category = "Other",
        street = "No Street Submited",
        city = "City",
        state = "AL",
        zip_code = "00000",
        phone = "",
        website = "")
    location.save()

    # Copy the default location image
    shutil.copyfile("static/media/images/main/location.jpg", "static/media/images/locations/" + str(location.id) + ".jpg")

    # Return the new location's ID
    return HttpResponse(location.id)


def send_email_verification_email_view(request, email = None):
    """Sends an email to the provided email allowing them to verify that email."""
    # Get the member who corresponds to the provided email (or raise a 404 error if no corresponding member exists)
    try:
        member = Member.active.get(username = email)
    except Member.DoesNotExist:
        raise Http404()

    # Send the member an email to verifiy their email address (or raise a 404 error if their email is already verified)
    if (member.verified == False):
        send_email_verification_email(member)
    else:
        raise Http404()

    return HttpResponse()


def send_update_email_verification_email_view(request, email = None):
    """Sends an email to the provided email allowing them to verify their new email."""
    # Get the member who corresponds to the provided email (or raise a 404 error if no corresponding member exists)
    try:
        member = Member.active.get(username = email)
    except Member.DoesNotExist:
        raise Http404()

    # Send the member an email to verifiy their email address (or raise a 404 error if their email is already verified)
    if (member.verified == False):
        send_update_email_verification_email(member)
    else:
        raise Http404()

    return HttpResponse()


def send_password_reset_email_view(request, email = None):
    """Sends an email to the provided email allowing the corresponding to reset their password."""
    # Get the member who corresponds to the provided email and send them an email to reset their password (otherwise, don't do anything)
    try:
        member = Member.active.get(username = email)
        send_password_reset_email(member)
    except Member.DoesNotExist:
        pass

    return HttpResponse()


def send_request_to_follow_email_view(request, to_member_id = None):
    """Sends an email to the provided email allowing the corresponding to reset their password."""
    # Get the member who is sending the follow request (or raise a 404 error if the member ID is invalid)
    try:
        from_member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    # Get the member to whom the follow request is being sent (or raise a 404 error if the member ID is invalid)
    try:
        to_member = Member.active.get(pk = to_member_id)
    except member.DoesNotExist:
        raise Http404()

    # If the from_member has actually requested to follow the to_member, send the request to follow email
    if (from_member in to_member.requested.all()):
        send_request_to_follow_email(from_member, to_member)
    else:
        raise Http404()

    return HttpResponse()


def send_accept_request_email_view(request, from_member_id = None):
    """Sends an email to the provided email allowing the corresponding to reset their password."""
    # Get the member who is accepting the follow request (or raise a 404 error if the member ID is invalid)
    try:
        to_member = Member.active.get(pk = request.session["member_id"])
    except:
        raise Http404()

    # Get the member to who sent the follow request (or raise a 404 error if the member ID is invalid)
    try:
        from_member = Member.active.get(pk = from_member_id)
    except member.DoesNotExist:
        raise Http404()

    # If the from_member is actually following the to_member, send the request accepted email
    if (from_member in to_member.followers.all()):
        send_accept_request_email(from_member, to_member)
    else:
        raise Http404()

    return HttpResponse()


def set_password_view(request):
    """Resets the member's password."""
    # Get the member corresponding to the provided email (or throw a 404 error)
    try:
        member = Member.active.get(pk = request.POST["memberID"])
    except:
        raise Http404()

    # Get the POST data
    password = request.POST["password"]
    confirm_password = request.POST["confirmPassword"]
    verification_hash = request.POST["verificationHash"]

    # If the passwords are long enough and match and the verification hash is correct, reset the member's password (or throw a 404 error)
    if ((len(password) >= 8) and (password == confirm_password) and (verification_hash == member.verification_hash)):
        member.set_password(password)
        member.save()
    else:
        raise Http404()
        
    return render_to_response( "resetPasswordConfirmation.html",
        { "m" : member },
        context_instance = RequestContext(request) )
