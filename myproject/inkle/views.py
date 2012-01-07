from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.shortcuts import render_to_response

from django.contrib.auth.models import User
from django.contrib import auth

from myproject.inkle.models import *
from myproject.inkle.choices import *

from myproject.inkle.emails import *

import random
import hashlib
import re

from django.db.models import Q

import datetime
import shutil

from databaseViews import *

def home_view(request):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
           return HttpResponseRedirect("/login")
    
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])
    
    member.num_requests = 0
    for r in member.requested.all():
        member.num_requests += 1

    member.spheres2 = member.spheres.all()
    member.circles2 = member.circles.all()

    # Get date objects for today, tomorrow, and the day after tomorrow 
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days = 1)
    day_after_tomorrow = today + datetime.timedelta(days = 2)

    # Get others' dinner inklings for today
    date = str(today.month) + "/" + str(today.day) + "/" + str(today.year)
    locations = get_others_inklings(member, date, "other", "circles", "dinner")

    return render_to_response( "home.html",
        { "member" : member, "locations" : locations, "today" : today, "tomorrow" : tomorrow, "dayAfterTomorrow" : day_after_tomorrow },
        context_instance = RequestContext(request) )

def manage_view(request, default_content_type = "circles"):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
          return HttpResponseRedirect("/login")

    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])
    member.spheres2 = member.spheres.all()

    member.num_requests = 0
    for r in member.requested.all():
        member.num_requests += 1

    return render_to_response( "manage.html",
        {"member" : member, "defaultContentType" : default_content_type},
        context_instance = RequestContext(request) )

def member_view(request, other_member_id = None):
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")
    
    # Get the member whose page the logged in member is viewing (or throw a 404 error if the member doesn't exist)
    try:
        other_member = Member.objects.get(pk = other_member_id)
    except:
        raise Http404()

    member.num_requests = 0
    for r in member.requested.all():
        member.num_requests += 1

    is_following = other_member in member.following.all()

    return render_to_response( "member.html",
        { "member" : member, "other_member" : other_member, "is_following" : is_following },
        context_instance = RequestContext(request) )
    
def location_view(request, location_id = None):
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])
    
    # If the location ID is invalid, throw a 404 error
    try:
        location = Location.objects.get(pk = location_id)
    except:
        raise Http404()

    now = datetime.datetime.now()
    date = str(now.month) + "/" + str(now.day) + "/" + str(now.year)
    
    people = member.following.all()
    dinnerPeople = [p for p in people if (p.inklings.filter(date = date, category = "dinner", location = location))]
    for m in dinnerPeople:
        m.spheres2 = m.spheres.all()
        m.show_contact_info = True
        m.mutual_followings = member.following.all() & m.following.all()
        m.button_list = []
    pregamePeople = [p for p in people if (p.inklings.filter(date = date, category = "pregame", location = location))]
    for m in pregamePeople:
        m.spheres2 = m.spheres.all()
        m.show_contact_info = True
        m.mutual_followings = member.following.all() & m.following.all()
        m.button_list = []
    maineventPeople = [p for p in people if (p.inklings.filter(date = date, category = "mainEvent", location = location))]
    for m in maineventPeople:
        m.spheres2 = m.spheres.all()
        m.show_contact_info = True
        m.mutual_followings = member.following.all() & m.following.all()
        m.button_list = []

    return render_to_response( "location.html",
        {"member" : member, "location" : location, "dinnerPeople" : dinnerPeople, "pregamePeople" : pregamePeople, "maineventPeople" : maineventPeople},
        context_instance = RequestContext(request) )


def get_edit_location_html_view(request):
    """Returns the edit location HTML."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")
    
    # Make sure the logged in member can update the location
    if (not member.is_staff):
        raise Http404()
    
    # Get the location (or throw a 404 error if the location ID is invalid)
    try:
        location = Location.objects.get(pk = request.POST["locationID"])
    except:
        raise Http404()
  
    return render_to_response( "editLocationInfo.html",
        {"member" : member, "location" : location, "states" : STATES, "categories" : LOCATION_CATEGORIES},
        context_instance = RequestContext(request) )


def get_edit_manage_html_view(request):
    """Returns the edit mange HTML."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")
    
    # Parse the birthday information
    member.month = member.birthday.split("/")[0]
    member.day = member.birthday.split("/")[1]
    member.year = member.birthday.split("/")[2]

    if member.month:
        member.month = int(member.month)
    else:
        member.month = 0
    if member.day:
        member.day = int(member.day)
    else:
        member.day = 0

    if member.year:
        member.year = int(member.year)
    else:
        member.year = 0

    if (member.month == 2):
        if (member.year == 0):
            member.day_range = range(1, 30)
        elif ((member.year % 4 != 0) or (member.year == 1900)):
            member.day_range = range(1, 29)
        else:
            member.day_range = range(1, 30)
    elif member.month in [4, 6, 9, 11]:
        member.day_range = range(1, 31)
    else:
        member.day_range = range(1, 32)

    today = datetime.date.today()
    member.year_range = range(1900, today.year + 1)

    return render_to_response( "editManageInfo.html",
        {"member" : member, "states" : STATES, "months" : MONTHS},
        context_instance = RequestContext(request) )


def search_view(request, query = ""):
    """Returns results for the logged in member's search query."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")
    
    # Determine how many requests the logged in member has
    member.num_requests = len(member.requested.all())

    # Strip the whitespace off the ends of the query
    query = query.strip()

    # Get the people who match the search query
    if (len(query.split()) == 1):
        members = Member.objects.filter(Q(first_name__startswith = query) | Q(last_name__startswith = query))
    elif (len(query.split()) == 2):
        query_split = query.split()
        members = Member.objects.filter((Q(first_name__startswith = query_split[0]) & Q(last_name__startswith = query_split[1])) | (Q(first_name__startswith = query_split[1]) & Q(last_name__startswith = query_split[0])))
    else:
        members = []

    member.num_following = 0
    member.num_followers = 0
    member.num_other_people = 0

    # Determine the information to show on each member's card
    for m in members:
        # Determine the names of the current member's spheres
        m.sphereNames = [s.name.split() for s in m.spheres.all()]

        # Determine the current member's people type and button list
        if ((m in member.following.all()) and (member in m.following.all())):
            m.people_type = "following follower"
            member.num_following += 1
            member.num_followers += 1
            m.show_contact_info = True
            m.button_list = [buttonDictionary["prevent"], buttonDictionary["stop"], buttonDictionary["circles"]]
        elif (m in member.following.all()):
            m.people_type = "following"
            member.num_following += 1
            m.show_contact_info = True
            m.button_list = [buttonDictionary["stop"], buttonDictionary["circles"]]
        elif (member in m.following.all()):
            m.people_type = "follower"
            member.num_followers += 1
            m.show_contact_info = True
            if (m in member.pending.all()):
                m.button_list = [buttonDictionary["prevent"], buttonDictionary["revoke"]]
            else:
                m.button_list = [buttonDictionary["prevent"], buttonDictionary["request"]]
        else:
            m.people_type = "other"
            member.num_other_people += 1
            if (m in member.pending.all()):
                m.button_list = [buttonDictionary["revoke"]]
            else:
                m.button_list = [buttonDictionary["request"]]

        #Add circles
        if (m in member.following.all()):
            m.circles_copy = [circle for circle in member.circles.all()]
            for circle in m.circles_copy:
                    circle.members_copy = circle.members.all()

        # Determine the mutual followings
        m.mutual_followings = member.following.all() & m.following.all()

    # Get the locations which match the search query
    locations = Location.objects.filter(Q(name__contains = query))
    
    # Get the spheres which match the search query
    spheres = Sphere.objects.filter(Q(name__contains = query))
    
    member.num_my_spheres = 0
    member.num_other_spheres = 0

    # Determine which spheres the logged in member has joined and set the button list accordingly
    for s in spheres:
        if (s in member.spheres.all()):
            s.sphere_type = "mySpheres"
            member.num_my_spheres += 1
            s.button_list = [buttonDictionary["leave"]]
        else:
            s.sphere_type = "otherSpheres"
            member.num_other_spheres += 1
            s.button_list = [buttonDictionary["join"]]

    return render_to_response( "search.html",
        {"member" : member, "query" : query, "members" : members, "locations" : locations, "spheres" : spheres},
        context_instance = RequestContext(request) )

def requests_view(request):
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")

    # Get the members who have requested to follow the logged in member
    requested_members = member.requested.all()
    
    # Get the members whom the the logged in member has requested to follow
    pending_members = member.pending.all()

    # For each requested member, determine their spheres, mutual followings, and button list and allow their contact info to be seen
    for m in requested_members:
        m.sphereNames = [sphere.name.split() for sphere in m.spheres.all()]
        m.mutual_followings = member.following.all() & m.following.all()
        m.button_list = [buttonDictionary["reject"], buttonDictionary["accept"]]
        m.show_contact_info = True
    
    # For each pending member, determine their spheres, mutual followings, and button list and allow their contact info to be seen
    for m in pending_members:
        m.sphereNames = [sphere.name.split() for sphere in m.spheres.all()]
        m.mutual_followings = member.following.all() & m.following.all()
        m.button_list = [buttonDictionary["revoke"]]
        if ((m in member.followers.all()) or (m in requested_members)):
            m.show_contact_info = True

    return render_to_response( "requests.html",
        {"requested_members" : requested_members, "pending_members" : pending_members},
        context_instance = RequestContext(request) )

def followers_view(request, other_member_id = None):
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")
    
    if (other_member_id):
        # Get the member whose page the logged in member is viewing (or throw a 404 error if the member doesn't exist)
        try:
            member = Member.objects.get(pk = other_member_id)
        except:
            raise Http404()
        members = [f.follower for f in member.followers.all()]
        member.is_other = True
        page_context = "otherFollowers"
    else:
        members = [f.follower for f in member.followers.all()]
        page_context = "myFollowers"

    for m in members:
        m.spheres2 = m.spheres.all()
         
        m.mutual_followings = member.following.all() & m.following.all()
        m.relationship = "friend"
        
        m.button_list = []
        m.button_list.append(buttonDictionary["prevent"])
        if m in member.pending.all():
            m.button_list.append(buttonDictionary["revoke"])
            m.relationship = "pending"
        elif m in member.following.all():
            m.button_list.append(buttonDictionary["stop"])
            m.relationship = "friend"
        else:
            m.button_list.append(buttonDictionary["request"])
            m.relationship = "other"
            
    return render_to_response( "followers.html",
        { "member" : member, "members" : members, "pageContext" : page_context },
        context_instance = RequestContext(request) )

def following_view(request, other_member_id = None):
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")
    
    if (other_member_id):
        # Get the member whose page the logged in member is viewing (or throw a 404 error if the member doesn't exist)
        try:
            member = Member.objects.get(pk = other_member_id)
        except:
            raise Http404()
        members = [f for f in member.following.all()]
    else:
        raise Http404()

    for m in members:
        m.spheres2 = m.spheres.all()
         
        m.mutual_followings = member.following.all() & m.following.all()
        m.relationship = "friend"
        
        m.button_list = []
        m.button_list.append(buttonDictionary["prevent"])
        if m in member.pending.all():
            m.button_list.append(buttonDictionary["revoke"])
            m.relationship = "pending"
        elif m in member.following.all():
            m.button_list.append(buttonDictionary["stop"])
            m.relationship = "friend"
        else:
            m.button_list.append(buttonDictionary["request"])
            m.relationship = "other"
            
    return render_to_response( "following.html",
        {"member" : member, "members" : members},
        context_instance = RequestContext(request) )
    
def circles_view(request):
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])
    
    circles = member.circles.all()
    
    for circle in circles:
        circle.ms = circle.members.all()

    members = member.accepted.all()
    for m in members:
        m.sphereNames = [s.name.split() for s in m.spheres.all()]
        m.show_contact_info = True
        m.mutual_followings = member.following.all() & m.following.all()
        m.button_list = [buttonDictionary["stop"], buttonDictionary["circles"]]
        m.circles_copy = [circle for circle in member.circles.all()]
        for circle in m.circles_copy:
            circle.members_copy = circle.members.all()

    return render_to_response( "circles.html",
        { "member" : member, "members" : members, "circles" : circles },
        context_instance = RequestContext(request) )

def circle_content_view(request):
    # Get the circle which was clicked
    circle_id = request.POST["circleID"]
    
    member = Member.objects.get(pk = request.session["member_id"])
    
    circle = None
    if (int(circle_id) == -1):
        members = member.accepted.all()
    else:
        circle = Circle.objects.get(pk = circle_id)
        members = circle.members.all()

    for m in members:
        m.sphereNames = [s.name.split() for s in m.spheres.all()]
        m.show_contact_info = True
        m.mutual_followings = member.following.all() & m.following.all()
        m.button_list = [buttonDictionary["stop"], buttonDictionary["circles"]]
        m.circles_copy = [circle for circle in member.circles.all()]
        for circle in m.circles_copy:
            circle.members_copy = circle.members.all()

    return render_to_response("circleContent.html", 
        {"circle" : circle, "members" : members},
        context_instance = RequestContext(request) )


def spheres_view(request, other_member_id = None):
    """Returns the spheres of which either the logged in  member or the member corresponding to the inputted member ID is a member."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")
    
    # If another member ID is inputted, get the spheres coresponding to that member
    if (other_member_id):
        # Get the member whose page the logged in member is viewing (or throw a 404 error if the member doesn't exist)
        try:
            other_member = Member.objects.get(pk = other_member_id)
        except:
            raise Http404()
        
        # Get the other memeber's spheres
        spheres = other_member.spheres.all()
        
        # Determine the button list for each sphere
        for s in spheres:
            if (s in member.spheres.all()):
                s.button_list = [buttonDictionary["leave"]]
            else:
                s.button_list = [buttonDictionary["join"]]

        # Specify the text if the other member is not in any spheres
        no_spheres_text = other_member.first_name + " " + other_member.last_name + " is"

        # Specify the page context
        page_context = "member"
    
    # Otherwise, if no member ID is inputted, get the spheres corresponding to the logged in member
    else:
        # Get the logged in member's spheres
        spheres = member.spheres.all()

        # Give each sphere the "Leave sphere" button
        for s in spheres:
            s.button_list = [buttonDictionary["leave"]]
        
        # Specify the text if the logged in member is not in any spheres
        no_spheres_text = "You are"

        # Specify the page context
        page_context = "manage"

    return render_to_response( "spheres.html",
        { "spheres" : spheres, "pageContext" : page_context, "noSpheresText" : no_spheres_text },
        context_instance = RequestContext(request) )


def suggestions_view(request, query = ""):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
           return HttpResponseRedirect("/login")

    query = request.POST["query"]
    query_type = request.POST["type"]

    categories = []

    # Strip the whitespace off the ends of the query
    query = query.strip()

    if (query_type == "inkling"):
        locations = Location.objects.filter(Q(name__contains = query))
        if (locations):
            categories.append((locations,))
            
        num_chars = 15
       
    # Header search suggestions
    elif (query_type == "search"):
        # If the query is only one word long, match the members' first or last names alone
        if (len(query.split()) == 1):
            members = Member.objects.filter(Q(first_name__startswith = query) | Q(last_name__startswith = query))
        elif (len(query.split()) == 2):
            query_split = query.split()
            members = Member.objects.filter((Q(first_name__startswith = query_split[0]) & Q(last_name__startswith = query_split[1])) | (Q(first_name__startswith = query_split[1]) & Q(last_name__startswith = query_split[0])))
        else:
            members = []

        # Add the members category to the search suggestions
        if (members):
            for m in members:
                m.name = m.first_name + " " + m.last_name
            categories.append((members, "Members"))
        
        locations = Location.objects.filter(Q(name__contains = query) | Q(city__contains = query))
        if (locations):
            categories.append((locations, "Locations"))

        spheres = Sphere.objects.filter(Q(name__contains = query))
        if (spheres):
            categories.append((spheres, "Spheres"))

        num_chars = 45

    elif (query_type == "addToCircle"):
        circle_id = request.POST["circleID"]
        circle = Circle.objects.get(pk = circle_id)

        member = Member.objects.get(pk = request.session["member_id"])
        following = member.following.all()
        circle_members = circle.members.all()
        people = list(set(following).difference(set(circle_members)))
       
        if (people):
            for p in people:
                p.name = p.first_name + " " + p.last_name
            categories.append((people,))

        num_chars = 10

    return render_to_response( "suggestions.html",
        { "categories" : categories, "numChars" : num_chars },
        context_instance = RequestContext(request) )

def get_others_inklings_view(request):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
           return HttpResponseRedirect("/login")
     
    # Get the logged in member
    member = Member.objects.get(pk = request.session["member_id"])

    # Get the POST data
    date = request.POST["date"]
    people_type = request.POST["peopleType"]
    people_id = request.POST["peopleID"]
    inkling_type = request.POST["inklingType"]
    include_member = request.POST["includeMember"]

    # Get others' inklings
    locations = get_others_inklings(member, date, people_type, people_id, inkling_type)

    member.spheres2 = member.spheres.all()
    member.circles2 = member.circles.all()

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
        people = member.following.all()

    elif (people_type == "sphere"):
        sphere = Sphere.objects.get(pk = people_id)
        people = sphere.member_set.all()
    
    elif (people_type == "circle"):
        circle = Circle.objects.get(pk = people_id)
        people = circle.members.all()

    locations = []
    for p in people:
        inkling = p.inklings.filter(date = date, category = inkling_type)
        if (inkling):
            location = inkling[0].location
            if (location in locations):
                for l in locations:
                    if (l == location):
                        l.count += 1
            else:
                location.count = 1
                locations.append(location)
    
    locations.sort(key = lambda l:-l.count)

    return locations

def login_view(request):
    """User login."""
    # If a user is already logged in, go to the main page
    if ("member_id" in request.session):
        return HttpResponseRedirect("/")
        
    # Initially say the login is valid
    invalid_login = False
    email = ""
    password = ""

    # Log the user in if they provided a valid username and password
    if (request.POST):
        # Get the POST data (and set the appropriate flag if the necessary POST data is not there)
        try:
            email = request.POST["email"]
        except:
            invalid_login = True

        try:
            password = request.POST["password"]
        except:
            invalid_login = True

        # Get the member with the provided username (or set the appropriate flag if it does not exist)
        if (not invalid_login):
            try:
                member = Member.objects.get(username = email)
            except:
                invalid_login = True
        
        # If the provided username exists and their password is correct, log them in (or set the appropriate flag if the password is incorrect)
        if ((not invalid_login) and (auth.authenticate(username = email, password = password)) and (member.verified)):
            request.session["member_id"] = member.id
            return HttpResponseRedirect("/")
        else:
            invalid_login = True
    
    # Create the year range
    today = datetime.date.today()
    year_range = range(1900, today.year + 1)

    return render_to_response( "login.html",
        {"selectedContentLink" : "login", "invalidLogin" : invalid_login, "loginEmail" : email, "loginPassword" : password, "dayRange" : range(1, 32), "yearRange" : year_range, "months" : MONTHS},
        context_instance = RequestContext(request) )


def request_password_reset_view(request):
    """Sends the HTML which enables a member to request a password reset email."""
    return render_to_response( "requestPasswordReset.html",
        {},
        context_instance = RequestContext(request) )


def password_reset_confirmation_view(request):
    """Returns a confirmation message saying an email has been sent to the inputted email so that the corresponding user can reset their password."""
    # Get the member who corresponds to the provided email
    email = request.POST["email"]
    try:
        member = Member.objects.get(username = email)
    except:
        pass
   
    return render_to_response( "passwordResetConfirmation.html",
        { "email" : email },
        context_instance = RequestContext(request) )

def reset_password_view(request, email = None, verification_hash = None):
    """Verifies a member's email address using the inputted verification hash."""
    # Get the member corresponding to the provided email (or raise a 404 error)
    try:
        member = Member.objects.get(username = email)
    except:
        raise Http404()

    # If the verification hash is correct, let the member reset their password 
    if (member.verification_hash == verification_hash):
        return render_to_response( "login.html",
            { "selectedContentLink" : "login", "loginContent" : "resetPassword", "m" : member },
            context_instance = RequestContext(request) )

    # Otherwise, if the hash is incorrect, raise a 404 error
    else:
        raise Http404()

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
        # Initially say the form data is valid
        invalid_first_name = False
        invalid_last_name = False
        invalid_email = False
        invalid_confirm_email = False
        invalid_password = False
        invalid_confirm_password = False
        invalid_month = False
        invalid_day = False
        invalid_year = False
        invalid_gender = False
        invalid_registration = False

        # Get the POST data (and set the appropriate flags if the necessary POST data is not there)
        try:
            first_name = request.POST["firstName"]
        except:
            first_name = ""
            invalid_first_name = True
            invalid_registration = True

        try:
            last_name = request.POST["lastName"]
        except:
            last_name = ""
            invalid_last_name = True
            invalid_registration = True

        try:
            email = request.POST["email"]
        except:
            email = ""
            invalid_email = True
            invalid_registration = True
            
        try:
            confirm_email = request.POST["confirmEmail"]
        except:
            confirm_email = ""
            invalid_confirm_email = True
            invalid_registration = True
            
        try:
            password = request.POST["password"]
        except:
            password = ""
            invalid_password = True
            invalid_registration = True
            
        try:
            confirm_password = request.POST["confirmPassword"]
        except:
            confirm_password = ""
            invalid_confirm_password = True
            invalid_registration = True
        
        try:
            month = request.POST["month"]
        except:
            month = ""
            invalid_month = True
            invalid_registration = True
        
        try:
            day = request.POST["day"]
        except:
            day = ""
            invalid_day = True
            invalid_registration = True
        
        try:
            year = request.POST["year"]
        except:
            year = ""
            invalid_year = True
            invalid_registration = True
            
        try:
            gender = request.POST["gender"]
        except:
            gender = ""
            invalid_registration = True

        # If any of the POST data is empty, set the appropriate flags
        if (first_name == ""):
            invalid_first_name = True
            invalid_registration = True
        if (last_name == ""):
            invalid_last_name = True
            invalid_registration = True
        if (email == ""):
            invalid_email = True
            invalid_registration = True
        if (confirm_email == ""):
            invalid_confirm_email = True
            invalid_registration = True
        if (password == ""):
            invalid_password = True
            invalid_registration = True
        if (confirm_password == ""):
            invalid_confirm_password = True
            invalid_registration = True
        if (month == ""):
            invalid_month = True
            invalid_registration = True
        if (day == ""):
            invalid_day = True
            invalid_registration = True
        if (year == ""):
            invalid_year = True
            invalid_registration = True
        if ((gender != "Male") and (gender != "Female")):
            invalid_gender = True
            invalid_registration = True

        # Check if the provided email already exists
        try:
            member = Member.objects.get(username = email)
        except:
            member = None
        if (member):
            invalid_email = True
            invalid_registration = True

        # Check if the provided email is a valid email address
        if (not re.search(r"[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+", email)):
            invalid_email = True
            invalid_registration = True
    
        # Check if the provided email matches the provided confirm email
        if (email != confirm_email):
            invalid_confirm_email = True
            invalid_registration = True
       
        # Check if the provided password is long enough (at least 8 characters)
        if (len(password) < 8):
            invalid_password = True
            invalid_confirm_password = True
            invalid_registration = True

        # Check if the provided password matches the provided confirm password
        if (password != confirm_password):
            invalid_confirm_password = True
            invalid_registration = True
    
        # Check if the user is at least sixteen years old
        if (day and month and year):
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
                invalid_day = True
                invalid_month = True
                invalid_year = True
                invalid_registration = True

        # If the registration form is valid, create a new member with the provided POST data
        if (not invalid_registration):
            # Create the verification hash
            verification_hash = hashlib.md5(str(random.randint(1000, 5000))).hexdigest()
           
            # Create the new member
            member = Member(
                first_name = first_name,
                last_name = last_name,
                username = email,
                email = email,
                birthday = month + "/" + day + "/" + year,
                gender = gender,
                verification_hash = verification_hash
            )
            
            # Set the new member's password
            member.set_password(password)

            # Create default image for the new member
            shutil.copyfile('static/media/images/members/default.jpg', 'static/media/images/members/' + str(member.id) + '.jpg')
            member.image = str(member.id) + ".jpg"

            # Save the new member
            member.save()

            # Send the new member an email to verify their email address
            send_email_verification_email(member)
                
            # Send the member to the successful account creation page
            return render_to_response( "registrationConfirmation.html",
                { "email" : email },
                context_instance = RequestContext(request) )

    # Parse the birthday data
    if month:
        month = int(month)
    else:
        month = 0
    if day:
        day = int(day)
    else:
        day = 0

    if year:
        year = int(year)
    else:
        year = 0

    if (month == 2):
        if (not year):
            day_range = range(1, 30)
        elif ((year % 4 != 0) or (year == 1900)):
            day_range = range(1, 29)
        else:
            day_range = range(1, 30)
    elif month in [4, 6, 9, 11]:
        day_range = range(1, 31)
    else:
        day_range = range(1, 32)

    today = datetime.date.today()
    year_range = range(1900, today.year + 1)

    return render_to_response( "registrationForm.html",
        {"selectedContentLink" : "registration", "invalidFirstName" : invalid_first_name, "firstName" : first_name, "invalidLastName" : invalid_last_name, "lastName" : last_name, "invalidEmail" : invalid_email, "email" : email, "invalidConfirmEmail" : invalid_confirm_email, "confirmEmail" : confirm_email, "invalidPassword" : invalid_password, "password" : password, "invalidConfirmPassword" : invalid_confirm_password, "confirmPassword" : confirm_password, "invalidMonth" : invalid_month, "month" : month, "months" : MONTHS, "invalidDay" : invalid_day, "day" : day, "dayRange" : day_range, "invalidYear" : invalid_year, "year" : year, "yearRange" : year_range, "invalidGender" : invalid_gender, "gender" : gender},
        context_instance = RequestContext(request) )


def verify_email_view(request, email = None, verification_hash = None):
    """Verifies a member's email address using the inputted verification hash."""
    # Get the member corresponding to the provided email (otherwise, throw a 404 error)
    try:
        member = Member.objects.get(username = email)
    except:
        raise Http404()

    # If the member has not yet been verified and the verification hash is correct, verify the member and give them a new verification hash(otherwise, throw a 404 error)
    if ((not member.verified) and (member.verification_hash == verification_hash)):
        member.verified = True
        member.verification_hash = hashlib.md5(str(random.randint(1000, 5000))).hexdigest()
        member.save()
    else:
        raise Http404()

    return render_to_response( "login.html",
        { "selectedContentLink" : "registration", "registrationContent" : "verifyEmail", "m" : member },
        context_instance = RequestContext(request) )


def logout_view(request):
    """Logs out the current user."""
    try:
        del request.session["member_id"]
    except:
        pass

    return HttpResponseRedirect("/login/")
