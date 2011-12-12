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
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])

    #print = request.POST["password"]

    member.first_name = request.POST["first_name"]
    member.last_name = request.POST["last_name"]
    #member.set_password(request.POST["password"])
    member.email = request.POST["email"]
    member.phone = request.POST["phone"]
    #member.birthday = request.POST["birthday"]
    member.gender = request.POST["gender"]
    member.save()
    
    return HttpResponse()

def edit_location_view(request, location_id = None):
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])
    
    # If the location ID is invalid, throw a 404 error
    try:
        location = Location.objects.get(pk = location_id)
    except:
        raise Http404()
    
    location.name = request.POST["name"]
    location.street = request.POST["street"]
    location.city = request.POST["city"]
    location.state = request.POST["state"]
    location.zip_code = int(request.POST["zipCode"])
    #location.phone = int(request.POST["phone"])
    #location.website = request.POST["website"]
    location.category = request.POST["category"]
    
    location.save()
    
    return HttpResponse()

def follow_request_view(request):
    # Get the member who is logged in
    from_member = Member.objects.get(pk = request.session["member_id"])

    # Get the member to whom the request is being sent
    to_member_id = request.POST["toMemberID"]
    to_member = Member.objects.get(pk = to_member_id)

    # Update the database to signify the request
    from_member.pending.add(to_member)
    to_member.requested.add(from_member)

    return HttpResponse(buttonDictionary["revoke"][2]) #Send updated toolTip information

def revoke_request_view(request):
    # Get the member who is logged in
    from_member = Member.objects.get(pk = request.session["member_id"])

    # Get the member to whom the request is being sent
    to_member_id = request.POST["toMemberID"]
    to_member = Member.objects.get(pk = to_member_id)

    # Update the database to signify the request
    from_member.pending.remove(to_member)
    to_member.requested.remove(from_member)

    return HttpResponse(buttonDictionary["request"][2]) #Send updated toolTip information

def accept_request_view(request):
    # Get the member who is logged in
    to_member = Member.objects.get(pk = request.session["member_id"])

    # Get the member to whom the request is being sent
    from_member_id = request.POST["fromMemberID"]
    from_member = Member.objects.get(pk = from_member_id)

    # Update the database to signify the accepted request
    from_member.pending.remove(to_member)
    from_member.accepted.add(to_member)
    to_member.requested.remove(from_member)
    from_follower = Follower(
                               follower = from_member,
                               count = 1
                           )
    from_follower.save()
    to_member.followers.add(from_follower)

    return HttpResponse()

def reject_request_view(request):
    # Get the member who is logged in
    to_member = Member.objects.get(pk = request.session["member_id"])

    # Get the member to whom the request is being sent
    from_member_id = request.POST["fromMemberID"]
    from_member = Member.objects.get(pk = from_member_id)

    # Update the database to signify the request
    from_member.pending.remove(to_member)
    to_member.requested.remove(from_member)

    return HttpResponse()
    
def stop_following_view(request):
    # Get the member who is logged in
    from_member = Member.objects.get(pk = request.session["member_id"])

    # Get the member who is being removed
    to_member_id = request.POST["toMemberID"]
    to_member = Member.objects.get(pk = to_member_id)

    # If the user is still in the accepted circle, remove them
    from_member.accepted.remove(to_member)

    #Remove from all of from_member's circles
    memberCircles = from_member.circles.all()
    for circle in memberCircles:
        circle.members.remove(to_member)

    #Remove from_member as a follower of to_member
    for f in to_member.followers.all():
        if from_member == f.follower:
            to_member.followers.remove(f)
            f.delete()

    return HttpResponse()

def prevent_following_view(request):
    # Get the member who is logged in
    to_member = Member.objects.get(pk = request.session["member_id"])

    # Get the member to whom the request is being sent
    from_member_id = request.POST["fromMemberID"]
    from_member = Member.objects.get(pk = from_member_id)

    if to_member in from_member.accepted.all():
        from_member.accepted.remove(to_member)


    # Remove to member from all of from members circles
    for c in from_member.circles.all():
        if to_member in c.members.all():
            c.members.remove(to_member)

    # Delete the from member follower
    # TODO: Get the follower corresponding to the from_member more efficiently
    for follower in to_member.followers.all():
        if (from_member == follower.follower):
            to_member.followers.remove(follower)
            follower.delete()
            break

    return HttpResponse()

def add_to_circle_view(request):
    # Get the member who is logged in
    from_member = Member.objects.get(pk = request.session["member_id"])

    # Get the member to whom the request is being sent
    to_member_id = request.POST["toMemberID"]
    to_member = Member.objects.get(pk = to_member_id)

    # Get the circle which the member is being added to
    circle_id = request.POST["circleID"]
    circle = Circle.objects.get(pk=circle_id)

    # Add them to the circle
    circle.members.add(to_member)

    if to_member in from_member.accepted.all(): #If the new member was only in "accepted"
        from_member.accepted.remove(to_member)
    else: #The member was already in one or more other circles
        #Get the list of all the to_member's followers, then choose the one corresponding to the current member
        #follower = [F for F in to_member.followers.all() if F.follower == from_member][0]
        follower = to_member.followers.filter(follower=from_member)[0]
        follower.count += 1
        follower.save()
    
    to_member.relationship = "friend"
    temp = [x for x in Member.objects.all() if (from_member in [y.follower for y in x.followers.all()] )]
    to_member.num_mutual_followings = len( [x for x in temp if to_member in [y.follower for y in x.followers.all()] ] )
    to_member.button_list = []
    to_member.button_list.append(buttonDictionary["stop"])
    #Add circles
    to_member.button_list.append(buttonDictionary["circles"])
    to_member.circles2 = [c for c in from_member.circles.all()]
    for c in to_member.circles2:
        c.members2 = c.members.all()
   
    return render_to_response("memberCard.html",
        { "m" : to_member },
        context_instance = RequestContext(request) )

    return HttpResponse()

def remove_from_circle_view(request):
    remove_from_circle(request.session["member_id"], request.POST["toMemberID"], request.POST["circleID"])
    return HttpResponse()

def remove_from_circle(from_member_id, to_member_id, circle_id):
    # Get the member who is logged in
    from_member = Member.objects.get(pk = from_member_id)

    # Get the member to whom the request is being sent
    to_member = Member.objects.get(pk = to_member_id)

    # Get the circle which the member is being added to
    circle = Circle.objects.get(pk=circle_id) #Retrieve the actual circle object

    circle.members.remove(to_member) # Remove them from the circle

    #Get the list of all the to_member's followers, then choose the one corresponding to the current member
    #follower = [F for F in to_member.followers.all() if F.follower == from_member][0]
    follower = to_member.followers.filter(follower=from_member)[0]

    if (follower.count == 1): #If this is the last remaining circle the to_member belongs to
        from_member.accepted.add(to_member)
    else:   #If the to_member belongs to one or more other circles
        follower.count -= 1
        follower.save()

def add_circle_view(request):
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])

    # Create the new circle
    circle = Circle(name = request.POST["circleName"])
    circle.save()

    # Add the new circle to the logged in member's circle
    member.circles.add(circle)

    return HttpResponse(circle.id)

def delete_circle_view(request):
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])

    circle = Circle.objects.get(pk = request.POST["circleID"])
    circleMembers = circle.members.all()
    for m in circleMembers:
        remove_from_circle(member, m.id, request.POST["circleID"])

    # Remove the circle from the logged in member's set of circles
    member.circles.remove(circle)
    
    circle.delete()

    return HttpResponse(circle.id)

def leave_sphere_view(request):
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])

    # Get the sphere which is being joined
    sphere_id = request.POST["sphereID"]
    sphere = Sphere.objects.get(pk = sphere_id)

    # Add the sphere to the current member's spheres
    member.spheres.remove(sphere)

    return HttpResponse()

def join_sphere_view(request):
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])

    # Get the sphere which is being joing
    sphere_id = request.POST["sphereID"]
    sphere = Sphere.objects.get(pk = sphere_id)

    # Add the sphere to the current member's spheres
    member.spheres.add(sphere)

    return HttpResponse()

def set_inkling_view(request):
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])
    
    # Get the type of inkling
    inkling_type = request.POST["inklingType"]

    # Get the location where the user is going
    location_id = request.POST["locationID"]
    location = Location.objects.get(pk = location_id)
    
    # Get the date
    date = request.POST["date"]

    # Get the event for the location/type/date combination
    event = Event.objects.filter(location = location, category = inkling_type, date = date)
    if (event):
        event = event[0]

    # If no event exists, create it
    else:
        print date
        event = Event(location = location, category = inkling_type, date = date)
        event.save()
    
    # See if the logged in member already has an event for the location/date combination
    conflictingEvent = member.events.filter(category = inkling_type, date = date)
    if (conflictingEvent):
        member.events.remove(conflictingEvent[0])

    # Add the event to the logged in member's events
    else:
        member.events.add(event)

    return HttpResponse(location.name)

def get_inklings_view(request):
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])
    
    # Get the date
    date = request.POST["date"]
    
    # Get the inklings
    dinnerLocation = ""
    pregameLocation = ""
    mainEventLocation = ""

    for event in member.events.filter(date = date):
        if (event.category == "dinner"):
            dinnerLocation = event.location.name
        elif (event.category == "pregame"):
            pregameLocation = event.location.name
        elif (event.category == "mainEvent"):
            mainEventLocation = event.location.name
   
    return HttpResponse(dinnerLocation + "&&&" +  pregameLocation + "&&&" + mainEventLocation)

def add_sphere_view(request):
    newSphere = Sphere(name=request.POST["sphereName"])
    newSphere.save()
    return HttpResponse(str(newSphere.name) + " sphere created")
    
def add_location_view(request):
    newLocation = Location(
        name=request.POST["locationName"],
        category = "Other",
        street = "No Street Submited",
        city = "City",
        state = "AL",
        zip_code = "00000",
        phone = 0,
        website = "None")
    newLocation.save()
    return HttpResponse(newLocation.id)
