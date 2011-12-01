from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404

from django.shortcuts import render_to_response

from django.contrib.auth.models import User
from django.contrib import auth

from finalProject.upforit.models import *
from finalProject.upforit.forms import *

import datetime

def home_view(request):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
           return HttpResponseRedirect("/upforit/login")
    
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
           return HttpResponseRedirect("/upforit/login")
    
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

def search_view(request):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
           return HttpResponseRedirect("/upforit/login")
    
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])

    members = Member.objects.all()

    for m in members:
        if m in member.pending.all():
            m.relationship = "pending"
        elif member in [f.follower for f in m.followers.all()]:
            m.relationship = "friend"
        else:
            m.relationship = "other"
        
        #Create necessary buttons for member cards
        #Items in list are tuples (class name, value)
        m.button_list = []
        if m.relationship == "other" and m != member:
            m.button_list.append(("requestToFollow", "Request to follow"))
        if m.relationship == "pending" and m != member:
            m.button_list.append(("revokeRequest", "Revoke Request"))
        if m.relationship == "friend" and m != member:
            m.button_list.append(("stopFollowing", "Stop following"))

        m.num_mutual_friends = len([x for x in m.followers.all() if (x in member.followers.all())])

    return render_to_response(
                                 "search.html",
                                 {
                                     "member" : member,
                                     "members" : members
                                 },
                                 context_instance = RequestContext(request)
                             )

def requested_view(request):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
           return HttpResponseRedirect("/upforit/login")
    
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
            return HttpResponseRedirect("/upforit/login")

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

def add_to_circle_view(request):
    # Get the member who is logged in
    from_member = Member.objects.get(pk = request.session["member_id"])
    
    # Get the member to whom the request is being sent
    to_member_id = request.POST["toMemberID"]
    to_member = Member.objects.get(pk = to_member_id)

    # Get the circle which the member is being removed from
    circle_id = request.POST["circleID"]

    # Add them from the circle
    circle.members.add(to_member)
 
    # If accepted circle
    if (int(circle_id) == -1):
        from_member.accepted.remove(to_member)

    # If other circle
    else:
        circle = Circle.objects.get(pk = circle_id)
        
        # TODO: clean this up; possibly use to_member.followers.filter()?
        for follower in to_member.followers.all():
            if (from_member == follower.follower):
                from_follower = follower
                break

        # Increment the count for the correct follower
        from_follower.count += 1
        from_follower.save()

    return render_to_response(
                                 "login.html",
                                 {},
                                 context_instance = RequestContext(request)
                             )

def remove_from_circle_view(request):
    # Get the member who is logged in
    from_member = Member.objects.get(pk = request.session["member_id"])
    
    # Get the member to whom the request is being sent
    to_member_id = request.POST["toMemberID"]
    to_member = Member.objects.get(pk = to_member_id)
    
    # TODO: Get the follower corresponding to the from_member
    for follower in to_member.followers.all():
        if (from_member == follower.follower):
            from_follower = follower
            break

    # Get the circle which the member is being removed from
    circle_id = request.POST["circleID"]
    
    # If accepted circle
    if (int(circle_id) == -1):
        from_member.accepted.remove(to_member)
        to_member.followers.remove(from_follower)
        from_follower.delete()

    # If other circle
    else:
        circle = Circle.objects.get(pk = circle_id)

        # Remove them from the circle
        circle.members.remove(to_member)

        if (from_follower.count == 1):
            to_member.followers.remove(from_follower)
            from_follower.delete()
        else:
            from_follower.count -= 1
            from_follower.save()

    return render_to_response(
                                 "login.html",
                                 {},
                                 context_instance = RequestContext(request)
                             )

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
        m.button_list.append(("remove", "Remove"))

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
    
    if (int(circle_id) == -1):
        member = Member.objects.get(pk = request.session["member_id"])
        members = member.accepted.all()
    else:
        circle = Circle.objects.get(pk = circle_id)
        members = circle.members.all()

    for m in members:
        m.relationship = "friend"
        m.num_mutual_friends = len([x for x in m.followers.all() if (x in member.followers.all())])
        m.button_list = []
        m.button_list.append(("remove", "Remove"))

    return render_to_response(
        "circleMembers.html",
        {
            "members" : members
        },
        context_instance = RequestContext(request)
    )

def login_view(request):
    """User login."""
    # If a user is already logged in, go to the main page
    if "member_id" in request.session:
        return HttpResponseRedirect("/upforit")
    
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
                    return HttpResponseRedirect("/upforit/")
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
                return HttpResponseRedirect("/upforit/")

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

    return HttpResponseRedirect("/upforit/login/")
