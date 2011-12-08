from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.shortcuts import render_to_response

from django.contrib.auth.models import User
from django.contrib import auth

from finalProject.inkle.models import *
from finalProject.inkle.forms import *

from django.db.models import Q

import datetime

def home_view(request):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
           return HttpResponseRedirect("/inkle/login")
    
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])

    locations = Location.objects.all()
    
    return render_to_response(
                                 "home.html",
                                 {
                                    "member" : member,
                                    "locations" : locations
                                 },
                                 context_instance = RequestContext(request)
                             )

def manage_view(request):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
           return HttpResponseRedirect("/inkle/login")
    
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])
    
    return render_to_response(
                                 "manage.html",
                                 {"member" : member,},
                                 context_instance = RequestContext(request)
                             )
    

def location_view(request, location_id = None):
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])
    
    # If the location ID is invalid, throw a 404 error
    try:
        location = Location.objects.get(pk = location_id)
    except:
        raise Http404()

    return render_to_response(
                                 "location.html",
                                 {
                                     "member" : member,
                                     "location" : location
                                 },
                                 context_instance = RequestContext(request)
                             )

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
    
    return render_to_response(
                                 "login.html",
                                 {},
                                 context_instance = RequestContext(request)
                             )

def search_view(request, query = ""):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
           return HttpResponseRedirect("/inkle/login")
    
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])

    members = Member.objects.filter(Q(username__contains = query) | Q(first_name__contains = query) | Q(last_name__contains = query))
    members.length = len(members)

    locations = Location.objects.filter(Q(name__contains = query) | Q(city__contains = query))
    locations.length = len(locations)
    
    spheres = Sphere.objects.filter(Q(name__contains = query))
    spheres.length = len(spheres)

    for m in members:
        m.button_list = []
        if m in member.pending.all() and m != member:
            m.relationship = "pending"
            m.button_list.append(("revokeRequest", "Revoke request"))
        elif member in [f.follower for f in m.followers.all()] and m != member:
            m.relationship = "friend"
            #Add circles
            m.button_list.append(("stopFollowing", "Stop following"))
            m.button_list.append(("circlesCardButton", "Circles"))
            m.circles2 = [c for c in member.circles.all()]
        elif m != member:
            m.relationship = "other"
            m.button_list.append(("requestToFollow", "Request to follow"))
        else:
            m.relationship = "self"
            
        # Prevent following
        if m in [f.follower for f in member.followers.all()]:
            m.button_list.append(("preventFollowing", "Prevent following"))

        m.num_mutual_friends = len([x for x in m.followers.all() if (x in member.followers.all())])

    for s in spheres:
        s.button_list = []
        if s in member.spheres.all():
            s.button_list.append(("leaveSphere", "Leave sphere"))
        else:
            s.button_list.append(("joinSphere", "Join sphere"))


    return render_to_response(
                                 "search.html",
                                 {
                                     "member" : member,
                                     "query" : query,
                                     "members" : members,
                                     "locations" : locations,
                                     "spheres" : spheres
                                 },
                                 context_instance = RequestContext(request)
                             )

def requested_view(request):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
           return HttpResponseRedirect("/inkle/login")
    
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])

    members = member.requested.all()

    for m in members:
        m.num_mutual_friends = len([x for x in m.followers.all() if (x in member.followers.all())])
        m.relationship = "pending"
        m.button_list = []
        m.button_list.append(("rejectRequest", "Reject request"))
        m.button_list.append(("acceptRequest", "Accept request"))

    return render_to_response(
                                 "requested.html",
                                 {
                                     "member" : member,
                                     "members" : members
                                 },
                                 context_instance = RequestContext(request)
                             )

def followers_view(request):
     # If a user is not logged in, redirect them to the login page
     if ("member_id" not in request.session):
            return HttpResponseRedirect("/inkle/login")

     # Get the member who is logged in
     member = Member.objects.get(pk = request.session["member_id"])

     members = [f.follower for f in member.followers.all()]

     for m in members:
         m.num_mutual_friends = len([x for x in m.followers.all() if (x in member.followers.all())])
         m.relationship = "friend"
         
         m.button_list = []
         m.button_list.append(("preventFollowing", "Prevent following"))

     return render_to_response(
                                  "followers.html",
                                  {
                                      "member" : member,
                                      "members" : members
                                  },
                                  context_instance = RequestContext(request)
                              )

def follow_request_view(request):
    # Get the member who is logged in
    from_member = Member.objects.get(pk = request.session["member_id"])
    
    # Get the member to whom the request is being sent
    to_member_id = request.POST["toMemberID"]
    to_member = Member.objects.get(pk = to_member_id)

    # Update the database to signify the request
    from_member.pending.add(to_member)
    to_member.requested.add(from_member)

    return render_to_response(
                                 "login.html",
                                 {},
                                 context_instance = RequestContext(request)
                             )

def revoke_request_view(request):
    # Get the member who is logged in
    from_member = Member.objects.get(pk = request.session["member_id"])
    
    # Get the member to whom the request is being sent
    to_member_id = request.POST["toMemberID"]
    to_member = Member.objects.get(pk = to_member_id)

    # Update the database to signify the request
    from_member.pending.remove(to_member)
    to_member.requested.remove(from_member)

    return render_to_response(
                                 "login.html",
                                 {},
                                 context_instance = RequestContext(request)
                             )

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

    return render_to_response(
                                 "login.html",
                                 {},
                                 context_instance = RequestContext(request)
                             )

def reject_request_view(request):
    # Get the member who is logged in
    to_member = Member.objects.get(pk = request.session["member_id"])
    
    # Get the member to whom the request is being sent
    from_member_id = request.POST["fromMemberID"]
    from_member = Member.objects.get(pk = from_member_id)

    # Update the database to signify the request
    from_member.pending.remove(to_member)
    to_member.requested.remove(from_member)

    return render_to_response(
                                 "login.html",
                                 {},
                                 context_instance = RequestContext(request)
                             )


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

    return render_to_response(
        "login.html",
        {},
        context_instance = RequestContext(request)
    )

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

    return render_to_response(
                                 "login.html",
                                 {},
                                 context_instance = RequestContext(request)
                             )

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

    return HttpResponse("")

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

    return HttpResponse("")
    
def circles_view(request):
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])
    
    circles = member.circles.all()
    
    for c in circles:
        c.ms = c.members.all()

    members = member.accepted.all()
    for m in members:
        m.relationship = "friend"
        m.num_mutual_friends = len([x for x in m.followers.all() if (x in member.followers.all())])
        m.button_list = []
        m.button_list.append(("stopFollowing", "Stop following"))
        #Add circles
        m.button_list.append(("circlesCardButton", "Circles"))
        m.circles2 = [c for c in member.circles.all()]
        for c in m.circles2:
                c.members2 = c.members.all()

    return render_to_response(
        "circles.html",
        {
            "member" : member,
            "members" : members,
            "circles" : circles
        },
        context_instance = RequestContext(request)
    )

def circle_members_view(request):
    # Get the circle which was clicked
    circle_id = request.POST["circleID"]
    
    member = Member.objects.get(pk = request.session["member_id"])
    
    if (int(circle_id) == -1):
        members = member.accepted.all()
    else:
        circle = Circle.objects.get(pk = circle_id)
        members = circle.members.all()

    for m in members:
        m.relationship = "friend"
        m.num_mutual_friends = len([x for x in m.followers.all() if (x in member.followers.all())])
        m.button_list = []
        m.button_list.append(("stopFollowing", "Stop following"))
        #Add circles
        m.button_list.append(("circlesCardButton", "Circles"))
        m.circles2 = [c for c in member.circles.all()]
        for c in m.circles2:
                c.members2 = c.members.all()

    return render_to_response(
        "circleMembers.html",
        {
            "members" : members
        },
        context_instance = RequestContext(request)
    )

def add_circle_view(request):
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])
    
    # Get the name of the new circle
    circle_name = request.POST["circleName"]

    # Create the new circle
    circle = Circle(name = circle_name)
    circle.save()

    # Add the new circle to the logged in member's circle
    member.circles.add(circle)

    return HttpResponse(circle.id)

def join_sphere_view(request):
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])
    
    # Get the sphere which is being joing
    sphere_id = request.POST["sphereID"]
    sphere = Sphere.objects.get(pk = sphere_id)

    # Add the sphere to the current member's spheres
    member.spheres.add(sphere)

    return render_to_response(
                                 "login.html",
                                 {},
                                 context_instance = RequestContext(request)
                             )

def leave_sphere_view(request):
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])
    
    # Get the sphere which is being joing
    sphere_id = request.POST["sphereID"]
    sphere = Sphere.objects.get(pk = sphere_id)

    # Add the sphere to the current member's spheres
    member.spheres.remove(sphere)

    return render_to_response(
                                 "login.html",
                                 {},
                                 context_instance = RequestContext(request)
                             )

def login_view(request):
    """User login."""
    # If a user is already logged in, go to the main page
    if "member_id" in request.session:
        return HttpResponseRedirect("/inkle")
    
    # If the POST data is empty, return an empty form
    if (not request.POST):
        log_form = login_form()
        reg_form = registration_form()
    
    # If the user has submitted POST data, see if the information is valid
    else:
        log_form = login_form(request.POST)
        if log_form.is_valid():
            # Check if a member with the given username already exists
            try:
                member = Member.objects.get(username = log_form.cleaned_data["email"])
            
                # If the member's credentials are correct, log them in and return them to the home page
                if (member.password == log_form.cleaned_data["password"]):
                    request.session["member_id"] = member.id
                    return HttpResponseRedirect("/inkle/")
            except:
                pass
        
        reg_form = registration_form(request.POST)
        if reg_form.is_valid():
            first_name = reg_form.cleaned_data["first_name"]
            last_name = reg_form.cleaned_data["last_name"]
            email = reg_form.cleaned_data["email"]
            email_verify = reg_form.cleaned_data["email_verify"]
            password = reg_form.cleaned_data["password"]
            gender = reg_form.cleaned_data["gender"]

            if (email == email_verify):
                member = Member(
                    first_name = first_name,
                    last_name = last_name,
                    username = email,
                    password = password,
                    email = email,
                    gender = gender
                )
                member.is_staff = True
                member.save()
                
                # Log the user in
                request.session["member_id"] = member.id
                return HttpResponseRedirect("/inkle/")

    return render_to_response(
                                 "login.html",
                                 {
                                     "login_form" : log_form,
                                     "registration_form" : reg_form
                                 },
                                 context_instance=RequestContext(request)
                             )

def logout_view(request):
    """Logs out the current user."""
    try:
        del request.session["member_id"]
    except:
        pass

    return HttpResponseRedirect("/inkle/login/")
