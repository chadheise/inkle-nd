from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.shortcuts import render_to_response

from django.contrib.auth.models import User
from django.contrib import auth

from finalProject.inkle.models import *
from finalProject.inkle.forms import *

from django.db.models import Q

import datetime

from databaseViews import *

def home_view(request):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
           return HttpResponseRedirect("/inkle/login")
    
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])
    
    member.num_requests = 0
    for r in member.requested.all():
        member.num_requests += 1

    member.spheres2 = member.spheres.all()
    member.circles2 = member.circles.all()
    
    # Get the logged in member's inklings for today
    now = datetime.datetime.now()
    date = str(now.month) + "/" + str(now.day) + "/" + str(now.year)
    member.dinnerName, member.dinnerImage, member.pregameName, member.pregameImage, member.mainEventName, member.mainEventImage = get_inklings(member, date)

    # Get others' dinner inklings for today
    locations = get_others_inklings(member, date, "other", "circles", "dinner")

    return render_to_response( "home.html",
        { "member" : member, "locations" : locations },
        context_instance = RequestContext(request) )

def manage_view(request, defaultContent = "circles"):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
          return HttpResponseRedirect("/inkle/login")

    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])
    member.spheres2 = member.spheres.all()

    member.num_requests = 0
    for r in member.requested.all():
        member.num_requests += 1

    return render_to_response( "manage.html",
        {"member" : member, "defaultContent" : defaultContent},
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

def search_view(request, query = ""):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
           return HttpResponseRedirect("/inkle/login")
    
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])

    member.num_requests = 0
    for r in member.requested.all():
        member.num_requests += 1

    split_query = query.split()
    if (len(split_query) == 1):
        members = Member.objects.filter(Q(first_name__contains = query) | Q(last_name__contains = query))
    else:
        members = Member.objects.filter(Q(first_name__contains = query) | Q(last_name__contains = query) | Q(first_name__contains = split_query[0]) | Q(last_name__contains = split_query[1]))
    members.length = len(members)

    locations = Location.objects.filter(Q(name__contains = query))
    locations.length = len(locations)
    
    spheres = Sphere.objects.filter(Q(name__contains = query))
    spheres.length = len(spheres)

    for m in members:
        m.button_list = []
        
        m.spheres2 = m.spheres.all()
        
        # Prevent following
        if member.followers.filter(follower=m):
            m.button_list.append(buttonDictionary["prevent"])
        
        if m in member.pending.all() and m != member:
            m.show_contact_info = False
            m.button_list.append(buttonDictionary["revoke"])
        elif ((m in member.following.all()) and (m != member)):
            m.relationship = "friend"
            #Add circles
            m.button_list.append(buttonDictionary["stop"])
            m.button_list.append(buttonDictionary["circles"])
            m.circles2 = [c for c in member.circles.all()]
            for c in m.circles2:
                    c.members2 = c.members.all()
        elif m != member:
            m.relationship = "other"
            m.button_list.append(buttonDictionary["request"])
        else:
            m.relationship = "self"
            
        m.mutual_followings = member.following.all() & m.following.all()

    for s in spheres:
        s.button_list = []
        if s in member.spheres.all():
            s.button_list.append(buttonDictionary["leave"])
        else:
            s.button_list.append(buttonDictionary["join"])


    return render_to_response( "search.html",
        {"member" : member, "query" : query, "members" : members, "locations" : locations, "spheres" : spheres},
        context_instance = RequestContext(request) )

def requests_view(request):
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/inkle/login/")

    # Get the members who have requested to follow the logged in member
    requested_members = member.requested.all()
    
    # Get the members whom the the logged in member has requested to follow
    pending_members = member.pending.all()

    # For each requested member, determine their spheres, mutual followings, and button list and allow their contact info to be seen
    for m in requested_members:
        m.sphereNames = [sphere.name for sphere in m.spheres.all()]
        m.mutual_followings = member.following.all() & m.following.all()
        m.button_list = [buttonDictionary["reject"], buttonDictionary["accept"]]
        m.show_contact_info = True
    
    # For each pending member, determine their spheres, mutual followings, and button list and allow their contact info to be seen
    for m in pending_members:
        m.sphereNames = [sphere.name for sphere in m.spheres.all()]
        m.mutual_followings = member.following.all() & m.following.all()
        m.button_list = [buttonDictionary["revoke"]]
        if ((m in member.followers.all()) or (m in requested_members)):
            m.show_contact_info = True

    return render_to_response( "requests.html",
        {"requested_members" : requested_members, "pending_members" : pending_members},
        context_instance = RequestContext(request) )

def followers_view(request):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
        return HttpResponseRedirect("/inkle/login")

    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])

    members = [f.follower for f in member.followers.all()]

    for m in members:
        m.spheres2 = m.spheres.all()
         
        m.mutual_followings = member.following.all() & m.following.all()
        m.relationship = "friend"
        
        m.button_list = []
        m.button_list.append(buttonDictionary["prevent"])
        if not m.followers.filter(follower = member):
            m.button_list.append(buttonDictionary["request"])
            m.relationship = "other"

    return render_to_response( "followers.html",
        {"member" : member, "members" : members},
        context_instance = RequestContext(request) )
    
def circles_view(request):
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])
    
    circles = member.circles.all()
    
    for c in circles:
        c.ms = c.members.all()

    members = member.accepted.all()
    for m in members:
        m.spheres2 = m.spheres.all()
        m.relationship = "friend"
        m.mutual_followings = member.following.all() & m.following.all()
        m.button_list = [buttonDictionary["stop"], buttonDictionary["circles"]]
        m.circles2 = [c for c in member.circles.all()]
        for c in m.circles2:
                c.members2 = c.members.all()

    return render_to_response( "circles.html",
        {"member" : member,"members" : members,"circles" : circles},
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
        m.spheres2 = m.spheres.all()
        m.relationship = "friend"
        m.mutual_followings = member.following.all() & m.following.all()
        m.button_list = []
        m.button_list.append(buttonDictionary["stop"])
        #Add circles
        m.button_list.append(buttonDictionary["circles"])
        m.circles2 = [c for c in member.circles.all()]
        for c in m.circles2:
                c.members2 = c.members.all()

    return render_to_response("circleContent.html", 
        {"circle" : circle, "members" : members},
        context_instance = RequestContext(request) )

def spheres_view(request):
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])

    spheres = member.spheres.all()

    for s in spheres:
        s.button_list = []
        s.button_list.append(buttonDictionary["leave"])

    return render_to_response( "spheres.html",
        {"member" : member,"spheres" : spheres},
        context_instance = RequestContext(request) )

def suggestions_view(request, query = ""):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
           return HttpResponseRedirect("/inkle/login")

    query = request.POST["query"]
    query_type = request.POST["type"]

    if (query_type == "inkling"):
        locations = Location.objects.filter(Q(name__contains = query))
        categories = [(locations,)]
        footerSubject = "Location"
        
    elif (query_type == "search"):
        categories = []

        people = Member.objects.filter(Q(username__contains = query) | Q(first_name__contains = query) | Q(last_name__contains = query))
        if (people):
            for p in people:
                p.name = p.first_name + " " + p.last_name
            categories.append((people, "People"))
        
        locations = Location.objects.filter(Q(name__contains = query) | Q(city__contains = query))
        if (locations):
            categories.append((locations, "Locations"))

        spheres = Sphere.objects.filter(Q(name__contains = query))
        if (spheres):
            categories.append((spheres, "Spheres"))
        
        footerSubject = ""

    elif (query_type == "addToCircle"):
        circle_id = request.POST["circleID"]
        circle = Circle.objects.get(pk = circle_id)

        member = Member.objects.get(pk = request.session["member_id"])
        following = member.following.all()
        circle_members = circle.members.all()
        people = list(set(following).difference(set(circle_members)))
       
        categories = []
        if (people):
            for p in people:
                p.name = p.first_name + " " + p.last_name
            categories = [(people,)]

        footerSubject = ""

    return render_to_response("suggestions.html",
        {"categories" : categories, "footerSubject" : footerSubject},
        context_instance = RequestContext(request) )

def get_others_inklings_view(request):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
           return HttpResponseRedirect("/inkle/login")
     
    # Get the logged in member
    member = Member.objects.get(pk = request.session["member_id"])

    # Get the POST data
    date = request.POST["date"]
    people_type = request.POST["peopleType"]
    people_id = request.POST["peopleID"]
    inkling_type = request.POST["inklingType"]

    # Get others' inklings
    locations = get_others_inklings(member, date, people_type, people_id, inkling_type)

    return render_to_response( "locationBoard.html",
        {"locations" : locations},
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
        return HttpResponseRedirect("/inkle/")
        
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
        if ((not invalid_login) and (member.password == password)):
            request.session["member_id"] = member.id
            return HttpResponseRedirect("/inkle/")
        else:
            invalid_login = True

    return render_to_response( "login.html",
        {"selectedContentLink" : "login", "invalidLogin" : invalid_login, "loginEmail" : email, "loginPassword" : password},
        context_instance=RequestContext(request) )

def register_view(request):
    """User login."""
    # If a user is already logged in, go to the main page
    if ("member_id" in request.session):
        return HttpResponseRedirect("/inkle/")
    
    # If there is no POST data, redirect the user to the login page
    if (not request.POST):
        return HttpResponseRedirect("/inkle/login/")
    
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

        # Check if the provided email matches the provided confirm email
        if (email != confirm_email):
            invalid_confirm_email = True
            invalid_registration = True
        
        # Check if the provided password matches the provided confirm password
        if (password != confirm_password):
            invalid_confirm_password = True
            invalid_registration = True

        # If the registration form is valid, create a new member with the provided POST data
        if (not invalid_registration):
            member = Member(
                first_name = first_name,
                last_name = last_name,
                username = email,
                password = password,
                email = email,
                birthday = month + "/" + day + "/" + year,
                gender = gender
            )
            
            # TODO: dont' make everyone staff by default!
            member.is_staff = True
            member.save()
                
            # Login the new member
            request.session["member_id"] = member.id
            return HttpResponseRedirect("/inkle/")

    return render_to_response( "login.html",
        {"selectedContentLink" : "registration", "invalidFirstName" : invalid_first_name, "firstName" : first_name, "invalidLastName" : invalid_last_name, "lastName" : last_name, "invalidEmail" : invalid_email, "email" : email, "invalidConfirmEmail" : invalid_confirm_email, "confirmEmail" : confirm_email, "invalidPassword" : invalid_password, "password" : password, "invalidConfirmPassword" : invalid_confirm_password, "confirmPassword" : confirm_password, "invalidMonth" : invalid_month, "month" : month, "invalidDay" : invalid_day, "day" : day, "invalidYear" : invalid_year, "year" : year, "invalidGender" : invalid_gender, "gender" : gender},
        context_instance=RequestContext(request) )

def logout_view(request):
    """Logs out the current user."""
    try:
        del request.session["member_id"]
    except:
        pass

    return HttpResponseRedirect("/inkle/login/")
