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
}

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

    return HttpResponse()

def remove_from_circle_view(request):
    # Get the member who is logged in
    from_member = Member.objects.get(pk = request.session["member_id"])

    # Get the member to whom the request is being sent
    to_member_id = request.POST["toMemberID"]
    to_member = Member.objects.get(pk = to_member_id)

    # Get the circle which the member is being added to
    circle_id = request.POST["circleID"]
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

    return HttpResponse()

def add_circle_view(request):
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])

    # Create the new circle
    circle = Circle(name = request.POST["circleName"])
    circle.save()

    # Add the new circle to the logged in member's circle
    member.circles.add(circle)

    return HttpResponse(circle.id)

def leave_sphere_view(request):
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])

    # Get the sphere which is being joing
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