from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.shortcuts import render_to_response

from django.contrib.auth.models import User
from django.contrib import auth

from finalProject.inkle.models import *
from finalProject.inkle.forms import *

buttonDictionary = {
    "request" : ("requestToFollow", "Request to follow", "Send a request to start following this person"),
    "prevent" : ("preventFollowing", "Prevent following", "No longer allow this person to follow me"),
    "revoke" : ("revokeRequest", "Revoke request", "Revoke my request to follow this person"),
    "stop" : ("stopFollowing", "Stop following", "Stop following this person"),
    "circles" : ("circlesCardButton", "Circles"),
    "reject" : ("rejectRequest", "Reject request", "Do not allow this person to follow me"),
    "accept" : ("acceptRequest", "Accept request", "Allow this person to follow me"),
    "join" : ("joinSphere", "Join sphere", "Beome a member of this sphere"),
    "leave" : ("leaveSphere", "Leave sphere", "I no longer wish to be a part of this sphere"),
}

def edit_profile_view(request):
    """Edits the logged in member's Member object."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/inkle/login/")

    # Update the logged in member's information using the POST data
    member.first_name = request.POST["first_name"]
    member.last_name = request.POST["last_name"]
    #member.set_password(request.POST["password"])
    member.email = request.POST["email"]
    member.phone = request.POST["phone"]
    member.birthday = request.POST["birthday"]
    member.gender = request.POST["gender"]
    
    # Save the logged in member's updated information
    member.save()
    
    return HttpResponse()


def edit_location_view(request):
    """Edits a location's Location object."""
    # TODO: make sure the logged in member can update the location
    
    # If the location ID is invalid, throw a 404 error
    location_id = request.POST["locationID"]
    try:
        location = Location.objects.get(pk = location_id)
    except:
        raise Http404()
   
    # Update the location's information using the POST data
    location.name = request.POST["name"]
    location.street = request.POST["street"]
    location.city = request.POST["city"]
    location.state = request.POST["state"]
    location.zip_code = int(request.POST["zipCode"])
    location.phone = request.POST["phone"]
    location.category = request.POST["category"]
    location.website = request.POST["website"]

    # Make sure the location begins with "http://www."
    if (location.website):
        if ((not location.website.startswith("http://")) and (not location.website.startswith("www"))):
            location.website = "http://www." + location.website
        elif (not location.website.startswith("http://")):
            location.website = "http://" + location.website
    
    # Save the location's updated information
    location.save()
    
    # Return the updated website
    return HttpResponse(location.website)


def request_to_follow_view(request):
    """Sends a request from the from_member to follow the to_member."""
    # Get the member who sent the request (or redirect them to the login page)
    try:
        from_member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/inkle/login/")

    # Get the member to whom the request is being sent
    to_member = Member.objects.get(pk = request.POST["toMemberID"])

    # Update the database to signify the request
    from_member.pending.add(to_member)
    to_member.requested.add(from_member)

    # Return the updated tooltip
    return HttpResponse(buttonDictionary["revoke"][2])


def revoke_request_view(request):
    """Revokes the request from the from_member to follow the to_member."""
    # Get the member who sent the request (or redirect them to the login page)
    try:
        from_member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/inkle/login/")

    # Get the member to whom the request was sent
    to_member = Member.objects.get(pk = request.POST["toMemberID"])

    # Update the database to signify the revoking of the request
    from_member.pending.remove(to_member)
    to_member.requested.remove(from_member)

    # Return the updated tooltip
    return HttpResponse(buttonDictionary["request"][2])


def accept_request_view(request):
    """Accepts the request from the from_member to follow the to_member."""
    # Get the member to whom the request was sent (or redirect them to the login page)
    try:
        to_member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/inkle/login/")

    # Get the member who sent the request
    from_member = Member.objects.get(pk = request.POST["fromMemberID"])

    # Update the database to signify the accepted request
    from_member.pending.remove(to_member)
    from_member.accepted.add(to_member)
    to_member.requested.remove(from_member)
    from_follower = Follower(follower = from_member, count = 1)
    from_follower.save()
    to_member.followers.add(from_follower)
    from_member.following.add(to_member)

    return HttpResponse()


def reject_request_view(request):
    """Rejects the request from the from_member to follow the to_member."""
    # Get the member to whom the request was sent (or redirect them to the login page)
    try:
        to_member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/inkle/login/")

    # Get the member who sent the request
    from_member = Member.objects.get(pk = request.POST["fromMemberID"])

    # Update the database to signify the request
    from_member.pending.remove(to_member)
    to_member.requested.remove(from_member)

    return HttpResponse()


def stop_following_view(request):
    """Makes the from_member stop following the to_member."""
    # Get the member who sent the request (or redirect them to the login page)
    try:
        from_member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/inkle/login/")

    # Get the member to whom the request was sent
    to_member = Member.objects.get(pk = request.POST["toMemberID"])

    # Make the from_member stop following the to_member
    remove_following(from_member, to_member)

    return HttpResponse()


def prevent_following_view(request):
    """Makes the from_member stop following the to_member."""
    # Get the member to whom the request was sent (or redirect them to the login page)
    try:
        to_member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/inkle/login/")

    # Get the member who sent the request
    from_member = Member.objects.get(pk = request.POST["fromMemberID"])

    # Make the from_member stop following the to_member
    remove_following(from_member, to_member)

    return HttpResponse()


def remove_following(from_member, to_member):
    """Makes the from_member stop following the to_member."""
    # Remove the to_member from the from_member's accepted list
    from_member.accepted.remove(to_member)

    # Remove the to_member from all of the from_member's circles
    for circle in from_member.circles.all():
        circle.members.remove(to_member)

    # Remove the from_member follower of to_member
    from_member_follower = to_member.followers.get(follower = from_member)
    to_member.followers.remove(from_member_follower)
    from_member_follower.delete()
    
    # Remove to_member from from_member's following list
    from_member.following.remove(to_member)

    return


def add_to_circle_view(request):
    """Adds the to_member to one of from_member's circles."""
    # Get the member who sent the request (or redirect them to the login page)
    try:
        from_member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/inkle/login/")

    # Get the member to whom the request was sent
    to_member = Member.objects.get(pk = request.POST["toMemberID"])

    # Get the circle to which to_member is being added
    circle = Circle.objects.get(pk = request.POST["circleID"])

    # Add the to_member to the circle
    circle.members.add(to_member)

    # If the to_member was only in the accepted list, remove them from the accepted list
    if (to_member in from_member.accepted.all()):
        from_member.accepted.remove(to_member)
    
    # Otherwise, increment the from_member's follower count
    else:
        from_member_follower = to_member.followers.get(follower = from_member)
        from_member_follower.count += 1
        from_member_follower.save()
    
    # Get the to_member's info for their member card
    to_member.sphereNames = [sphere.name for sphere in to_member.spheres.all()]
    to_member.mutual_followings = from_member.following.all() & to_member.following.all()
    to_member.button_list = [buttonDicationary["circles"], buttonDictionary["stop"]]
    to_member.show_contact_info = True
    to_member.circles2 = [circle for circle in from_member.circles.all()]
    for circle in to_member.circles2:
        circle.members2 = circle.members.all()
   
    return render_to_response( "memberCard.html",
        { "m" : to_member },
        context_instance = RequestContext(request) )

    return HttpResponse()


def remove_from_circle_view(request):
    """Removes the to_member from one of from_member's circles."""
    # Get the member who sent the request (or redirect them to the login page)
    try:
        from_member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/inkle/login/")

    # Get the member to whom the request was sent
    to_member = Member.objects.get(pk = request.POST["toMemberID"])
    
    # Get the circle to which to_member is being removed
    circle = Circle.objects.get(pk = request.POST["circleID"])

    # Remove the to_member from the from_member's circle
    remove_from_circle(from_member, to_member, circle)

    return HttpResponse()


def remove_from_circle(from_member, to_member, circle):
    """Removes the to_member from one of from_member's circles."""
    # Remove the to_member from the from_member's circle
    circle.members.remove(to_member)

    # Get the from_member's follower of to_member
    from_member_follower = to_member.followers.get(follower = from_member)

    # Add the to_member to the from_member's accepted list if this is the last circle the to_member belongs to
    if (from_member_follower.count == 1):
        from_member.accepted.add(to_member)

    # Otherwise, decrement the from_member's follower count
    else:
        from_member_follower.count -= 1
        from_member_follower.save()

    return


def create_circle_view(request):
    """Create a new circle for the logged in member."""
    # Get the logged in member (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/inkle/login/")

    # Create the new circle
    circle = Circle(name = request.POST["circleName"])
    circle.save()

    # Add the new circle to the logged in member's circles list
    member.circles.add(circle)

    # Return the new circle's ID
    return HttpResponse(circle.id)


def delete_circle_view(request):
    """Deletes one of the logged in member's circles."""
    # Get the logged in member (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/inkle/login/")

    # Get the circle which is to be deleted
    circle = Circle.objects.get(pk = request.POST["circleID"])

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
    # Get the logged in member (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/inkle/login/")

    # Get the sphere which is being joined
    sphere = Sphere.objects.get(pk = request.POST["sphereID"])

    # Add the sphere to the logged in member's spheres list
    member.spheres.add(sphere)

    return HttpResponse()


def leave_sphere_view(request):
    """Makes the logged in member leave a sphere."""
    # Get the logged in member (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/inkle/login/")

    # Get the sphere which is being left
    sphere = Sphere.objects.get(pk = request.POST["sphereID"])

    # Remove the sphere from the logged in member's spheres list
    member.spheres.remove(sphere)

    return HttpResponse()


def create_inkling_view(request):
    """Adds an inkling to the logged in member's inklings."""
    # Get the logged in member (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/inkle/login/")
   
    # Get the POST data
    inkling_type = request.POST["inklingType"]
    location = Location.objects.get(pk = request.POST["locationID"])
    date = request.POST["date"]

    # Get the inkling for the location/type/date combination (or create it if no inkling exists)
    try:
        # TODO: change filter to get and remove [0]???
        inkling = Inkling.objects.filter(location = location, category = inkling_type, date = date)[0]
    except:
        inkling = Inkling(location = location, category = inkling_type, date = date)
        inkling.save()
    
    # See if the logged in member already has an inkling for the location/date combination
    # TODO: change to get instead of filter and get rid of try/except
    try:
        conflicting_inkling = member.inklings.filter(category = inkling_type, date = date)[0]
        if (conflicting_inkling != inkling):
            remove_inkling(member, conflicting_inkling)
    except:
        pass

    # Add the inkling to the logged in member's inklings list
    member.inklings.add(inkling)

    # Return the location's name and image
    return HttpResponse(location.name + "&&&" + location.image)


def remove_inkling_view(request):
    """Removes an inkling from the logged in member's inklings."""
    # Get the logged in member (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/inkle/login/")
    
    # Get the POST data
    inkling_type = request.POST["inklingType"]
    date = request.POST["date"]
    
    # Get the inkling for the member/type/date combination and remove it if possible
    # TODO: replace filter with get
    try:
        inkling = member.inklings.filter(category = inkling_type, date = date)[0]
        remove_inkling(member, inkling)
    except:
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


def get_inklings_view(request):
    """Returns the logged in member's inklings for the inputted date."""
    # Get the logged in member (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/inkle/login/")
    
    # Get the POST data
    date = request.POST["date"]
    
    # Get the names and images for the logged in member's inkling locations
    dinnerName, dinnerImage, pregameName, pregameImage, mainEventName, mainEventImage = get_inklings(member, date)

    # Return the names and images for the logged in member's inkling locations
    return HttpResponse(dinnerName + "&&&" +  dinnerImage + "&&&" + pregameName + "&&&" + pregameImage + "&&&" + mainEventName + "&&&" + mainEventImage)


def get_inklings(member, date):
    """Returns the names and images for the logged in member's inkling locations."""
    # Get the name and image for the logged in member's dinner inkling location
    # TODO: replace filter with get
    try:
        inkling = member.inklings.filter(date = date, category = "dinner")[0]
        dinnerName = inkling.location.name
        dinnerImage = inkling.location.image
    except:
        dinnerName = ""
        dinnerImage = "default.jpg"
    
    # Get the name and image for the logged in member's pregame inkling location
    # TODO: replace filter with get
    try:
        inkling = member.inklings.filter(date = date, category = "pregame")[0]
        pregameName = inkling.location.name
        pregameImage = inkling.location.image
    except:
        pregameName = ""
        pregameImage = "default.jpg"

    # Get the name and image for the logged in member's main event inkling location
    # TODO: replace filter with get
    try:
        inkling =  member.inklings.filter(date = date, category = "mainEvent")[0]
        mainEventName = inkling.location.name
        mainEventImage = inkling.location.image
    except:
        mainEventName = ""
        mainEventImage = "default.jpg"


    # Return the names and images for the logged in member's inkling locations
    return (dinnerName, dinnerImage, pregameName, pregameImage, mainEventName, mainEventImage)


def create_sphere_view(request):
    """Creates a new Sphere object."""
    # Create a new sphere using the POST data and save it
    sphere = Sphere(name = request.POST["sphereName"])
    sphere.save()

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

    # Return the new location's ID
    return HttpResponse(location.id)
