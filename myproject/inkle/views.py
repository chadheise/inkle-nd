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
    """Gets dates objects and others' inkling locations and returns the HTML for the home page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")
    
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
    """Returns the HTML for the manage page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")

    return render_to_response( "manage.html",
        {"member" : member, "defaultContentType" : default_content_type},
        context_instance = RequestContext(request) )


def member_view(request, other_member_id = None):
    """Returns the HTML for the member page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")
    
    # Get the member whose page is being viewed (or throw a 404 error if their member ID is invalid)
    try:
        other_member = Member.objects.get(pk = other_member_id)
    except:
        raise Http404()

    # Redirect the logged in member to their profile page if they are the other member
    if (member == other_member):
        return HttpResponseRedirect("/manage/")

    return render_to_response( "member.html",
        { "member" : member, "other_member" : other_member },
        context_instance = RequestContext(request) )
    

def location_view(request, location_id = None):
    """Gets the members who are going to the inputted location today and returns the HTML for the location page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")
    
    # Get the location corresponding to the inputted ID (or throw a 404 error if it is invalid)
    try:
        location = Location.objects.get(pk = location_id)
    except:
        raise Http404()

    # Get today's date
    now = datetime.datetime.now()
    date = str(now.month) + "/" + str(now.day) + "/" + str(now.year)
    
    # Get the people who the logged in member is following
    following = member.following.all()

    # Get all of the specified date's inklings at the provided location
    location_inklings = Inkling.objects.filter(date = date, location = location)

    # Get the logged in member's dinner inkling and the members who are attending
    try:
        dinner_inkling = location_inklings.get(category = "dinner")
        all_dinner_members = dinner_inkling.member_set.all()
        member.dinner_members = [m for m in all_dinner_members if (m in following)]
        member.num_dinner_others = len(all_dinner_members) - len(member.dinner_members)
        for m in member.dinner_members:
            m.show_contact_info = True
            m.mutual_followings = member.following.all() & m.following.all()
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
            m.mutual_followings = member.following.all() & m.following.all()
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
            m.mutual_followings = member.following.all() & m.following.all()
            m.button_list = [buttonDictionary["circles"]]
    except Inkling.DoesNotExist:
        member.main_event_members = []
        member.num_main_event_others = 0

    return render_to_response( "location.html",
        { "member" : member, "location" : location },
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
    """Returns the edit manage HTML."""
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
 

def members_search_query(query):
    """Returns the members who match the inputted query."""
    # Split the query into words
    query_split = query.split()
    
    # If the query is only one word long, match the members' first or last names alone
    if (len(query_split) == 1):
        members = Member.objects.filter(Q(first_name__istartswith = query) | Q(last_name__istartswith = query))

    # If the query is two words long, match the members' first and last names
    elif (len(query_split) == 2):
        members = Member.objects.filter((Q(first_name__istartswith = query_split[0]) & Q(last_name__istartswith = query_split[1])) | (Q(first_name__istartswith = query_split[1]) & Q(last_name__istartswith = query_split[0])))
    
    # if the query is more than two words long, return no results
    else:
        members = []

    return members


def locations_search_query(query):
    """Returns the locations which match the inputted query."""
    locations = Location.objects.filter(Q(name__icontains = query))
    return locations
        

def spheres_search_query(query):
    """Returns the spheres which match the inputted query."""
    spheres = Sphere.objects.filter(Q(name__icontains = query))
    return spheres


def search_view(request, query = ""):
    """Gets the members, locations, and spheres which match the inputted query and returns the HTML for the search page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")
    
    # Strip the whitespace off the ends of the query
    query = query.strip()

    # Get the members who match the search query
    members = members_search_query(query)

    # Initialize member variables
    member.num_following = 0
    member.num_followers = 0
    member.num_other_people = 0

    # Determine each member's people type and button list
    for m in members:
        # Case 1: The logged in member is following and is being followed by the current member
        if ((m in member.following.all()) and (member in m.following.all())):
            m.people_type = "following follower"
            member.num_following += 1
            member.num_followers += 1
            m.show_contact_info = True
            #m.button_list = [buttonDictionary["prevent"], buttonDictionary["stop"], buttonDictionary["circles"]]
            m.button_list = [buttonDictionary["circles"]]

        # Case 2: The logged member is following the current member
        elif (m in member.following.all()):
            m.people_type = "following"
            member.num_following += 1
            m.show_contact_info = True
            #m.button_list = [buttonDictionary["stop"], buttonDictionary["circles"]]
            m.button_list = [buttonDictionary["circles"]]

        # Case 3: The logged member is being followed by the current member
        elif (member in m.following.all()):
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
        m.mutual_followings = member.following.all() & m.following.all()

    # Get the locations which match the search query
    locations = Location.objects.filter(Q(name__contains = query))
    
    # Get the spheres which match the search query
    spheres = Sphere.objects.filter(Q(name__contains = query))
    
    # Initialize member variables
    member.num_my_spheres = 0
    member.num_other_spheres = 0

    # Determine which spheres the logged in member has joined and set their button lists accordingly
    for sphere in spheres:
        if (sphere in member.spheres.all()):
            sphere.sphere_type = "mySpheres"
            member.num_my_spheres += 1
            sphere.button_list = [buttonDictionary["leave"]]
        else:
            sphere.sphere_type = "otherSpheres"
            member.num_other_spheres += 1
            sphere.button_list = [buttonDictionary["join"]]

    return render_to_response( "search.html",
        {"member" : member, "query" : query, "members" : members, "locations" : locations, "spheres" : spheres},
        context_instance = RequestContext(request) )


def suggestions_view(request):
    """Returns suggestions for the inputted query."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
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
        locations = locations_search_query(query)
        if (locations):
            categories.append((locations,))
        
        # Set the number of characters to show for each suggestion
        num_chars = 15
       
    # Case 2: Member, location, and sphere suggestions for the main header search
    elif (query_type == "search"):
        # Get the member suggestions (and add them to the categories list if there are any)
        members = members_search_query(query)
        if (members):
            for m in members:
                m.name = m.first_name + " " + m.last_name
            categories.append((members, "People"))
        
        # Get the location suggestions (and add them to the categories list if there are any)
        locations = locations_search_query(query)
        if (locations):
            categories.append((locations, "Locations"))

        # Get the sphere suggestions (and add them to the categories list if there are any)
        spheres = Sphere.objects.filter(Q(name__contains = query))
        if (spheres):
            categories.append((spheres, "Spheres"))

        # Set the number of characters to show for each suggestion
        num_chars = 45

    # Case 3: Member suggestions for adding members to circles
    elif (query_type == "addToCircle"):
        # Get the requested circle (or throw a 404 error if the circle ID is invalid)
        try:
            circle = Circle.objects.get(pk = request.POST["circleID"])
        except:
            raise Http404()
            
        # Get the members who match the search query and who are not already in the requested circle (and add them to the categories list if there are any)
        members = members_search_query(query)
        members = list(set(members) - set(circle.members.all()))
        if (members):
            for m in members:
                m.name = m.first_name + " " + m.last_name
            categories.append((members,))

        # Set the number of characters to show for each suggestion
        num_chars = 20

    return render_to_response( "suggestions.html",
        { "categories" : categories, "numChars" : num_chars },
        context_instance = RequestContext(request) )


def requests_view(request):
    """Gets the logged in member's request and returns the HTML for the requests page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")

    # Get the members who have requested to follow the logged in member
    requested_members = member.requested.all()
    
    # For each requested member, determine their spheres, mutual followings, and button list and allow their contact info to be seen
    for m in requested_members:
        m.mutual_followings = member.following.all() & m.following.all()
        m.button_list = [buttonDictionary["reject"], buttonDictionary["accept"]]
        if (m in member.following.all()):
            m.show_contact_info = True
        else:
            m.show_contact_info = False
    
    # Get the members whom the the logged in member has requested to follow
    pending_members = member.pending.all()

    # For each pending member, determine their spheres, mutual followings, and button list and allow their contact info to be seen
    for m in pending_members:
        m.mutual_followings = member.following.all() & m.following.all()
        m.button_list = [buttonDictionary["revoke"]]
        m.show_contact_info = False

    return render_to_response( "requests.html",
        { "requestedMembers" : requested_members, "pendingMembers" : pending_members },
        context_instance = RequestContext(request) )


def followers_view(request, other_member_id = None):
    """Gets the logged in member's or other member's followers and returns the HTML for the followers page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")
   
    # If we are viewing another member's page, get the members who are following them
    if (other_member_id):
        # Get the member whose page is being viewed (or throw a 404 error if their member ID is invalid)
        try:
            other_member = Member.objects.get(pk = other_member_id)
        except Member.DoesNotExist:
            raise Http404()

        # Get the members who are following the member whose page we are on and set the appropriate page context and no followers text
        members = other_member.followers.all()
        page_context = "otherFollowers"
        no_followers_text = other_member.first_name + " " + other_member.last_name

    # Otherwise, get the members who are following the logged in member and set the appropriate page context and no followers text
    else:
        members = member.followers.all()
        page_context = "myFollowers"
        no_followers_text = "you"

    # Get the necessary information for each member's member card
    for m in members:
        # Case 1: The logged in member is the current member
        if (m == member):
            m.button_list = []
            m.show_contact_info = True

        # Case 2: The logged in member has a pending request to follow the current member
        elif (m in member.pending.all()):
            m.button_list = [buttonDictionary["prevent"], buttonDictionary["revoke"]]
            m.show_contact_info = False

        # Case 3: The logged in member is following the current member
        elif (m in member.following.all()):
            m.button_list = [buttonDictionary["prevent"], buttonDictionary["circles"]]
            m.show_contact_info = True

        # Case 4: The logged in member is not following and has not requested to follow the current member
        else:
            m.button_list = [buttonDictionary["prevent"], buttonDictionary["request"]]
            m.show_contact_info = False
            
        # Determine the members who are being followed by both the logged in member and the current member
        m.mutual_followings = member.following.all() & m.following.all()

    return render_to_response( "followers.html",
        { "member" : member, "members" : members, "pageContext" : page_context, "noFollowersText" : no_followers_text },
        context_instance = RequestContext(request) )


def following_view(request, other_member_id = None):
    """Gets the logged in member's or other member's following and returns the HTML for the following page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")
    
    # Get the member whose page is being viewed (or throw a 404 error if their member ID is invalid)
    try:
        other_member = Member.objects.get(pk = other_member_id)
    except Member.DoesNotExist:
        raise Http404()

    # Get the members whom the other member is following
    members = [m for m in other_member.following.all()]

    # Get the necessary information for each member's member card
    for m in members:
        # Case 1: The logged in member is the current member
        if (m == member):
            m.button_list = []
            m.show_contact_info = True

        # Case 2: The logged in member has a pending request to follow the current member
        elif (m in member.pending.all()):
            m.button_list = [buttonDictionary["prevent"], buttonDictionary["revoke"]]
            m.show_contact_info = False

        # Case 3: The logged in member is following the current member
        elif (m in member.following.all()):
            m.button_list = [buttonDictionary["prevent"], buttonDictionary["circles"]]
            m.show_contact_info = True

        # Case 4: The logged in member is not following and has not requested to follow the current member
        else:
            m.button_list = [buttonDictionary["prevent"], buttonDictionary["request"]]
            m.show_contact_info = False
            
        # Determine the members who are being followed by both the logged in member and the current member
        m.mutual_followings = member.following.all() & m.following.all()

    return render_to_response( "following.html",
        { "member" : member, "otherMember" : other_member, "members" : members },
        context_instance = RequestContext(request) )

    
def circles_view(request, circle_id = None):
    """Gets the logged in member's circles returns the HTML for the circles page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")

    # If a circle ID is specified, get the members in that circle (otherwise, get the members in the logged in member's accepted circle)
    if (circle_id):
        circle = Circle.objects.get(pk = circle_id)
        members = circle.members.all()
    else:
        circle = []
        members = member.accepted.all()

    # Get the necessary information for each member's member card
    for m in members:
        # Show the logged in member's contact information
        m.show_contact_info = True

        # Show the "Stop following" and "Circles" buttons
        m.button_list = [buttonDictionary["stop"], buttonDictionary["circles"]]

        # Determine the members who are being followed by both the logged in member and the current member
        m.mutual_followings = member.following.all() & m.following.all()

    # If a circle ID is specified, return only the circle content (otherwise, return the entire HTML for the circles page)
    try:
        content = request.POST["content"]
        html = "circleContent.html"
    except KeyError:
        html = "circles.html"

    return render_to_response( html, 
        { "member" : member, "members" : members, "circle" : circle },
        context_instance = RequestContext(request) )


def spheres_view(request, other_member_id = None):
    """Gets the logged in member's or other member's spheres and returns the HTML for the sphere page."""
    # Get the member who is logged in (or redirect them to the login page)
    try:
        member = Member.objects.get(pk = request.session["member_id"])
    except:
        return HttpResponseRedirect("/login/")
   
    # If we are viewing another member's page, get the members who are following them
    if (other_member_id):
        # Get the member whose page is being viewed (or throw a 404 error if their member ID is invalid)
        try:
            other_member = Member.objects.get(pk = other_member_id)
        except Member.DoesNotExist:
            raise Http404()

        # Get the other member's spheres
        spheres = other_member.spheres.all()

        # Determine the button list for each sphere
        for s in spheres:
            if (s in member.spheres.all()):
                s.button_list = [buttonDictionary["leave"]]
            else:
                s.button_list = [buttonDictionary["join"]]

        # Specify the page context
        page_context = "member"

        # Specify the text if the other member is not in any spheres
        no_spheres_text = other_member.first_name + " " + other_member.last_name + " is"
    
    # Otherwise, if no member ID is inputted, get the spheres corresponding to the logged in member
    else:
        # Get the logged in member's spheres
        spheres = member.spheres.all()

        # Give each sphere the "Leave sphere" button
        for s in spheres:
            s.button_list = [buttonDictionary["leave"]]

        # Specify the page context
        page_context = "manage"
        
        # Specify the text if the logged in member is not in any spheres
        no_spheres_text = "You are"

    return render_to_response( "spheres.html",
        { "spheres" : spheres, "pageContext" : page_context, "noSpheresText" : no_spheres_text },
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
        except KeyError:
            invalid_login = True

        try:
            password = request.POST["password"]
        except KeyError:
            invalid_login = True

        # Get the member with the provided username (or set the appropriate flag if it does not exist)
        if (not invalid_login):
            try:
                member = Member.objects.get(username = email)
            except Member.DoesNotExist:
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
   
    return render_to_response( "passwordResetConfirmation.html",
        { "email" : email },
        context_instance = RequestContext(request) )

def reset_password_view(request, email = None, verification_hash = None):
    """Verifies a member's email address using the inputted verification hash."""
    # Get the member corresponding to the provided email (or raise a 404 error)
    try:
        member = Member.objects.get(username = email)
    except Member.DoesNotExist:
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
        except KeyError:
            first_name = ""
            invalid_first_name = True
            invalid_registration = True

        try:
            last_name = request.POST["lastName"]
        except KeyError:
            last_name = ""
            invalid_last_name = True
            invalid_registration = True

        try:
            email = request.POST["email"]
        except KeyError:
            email = ""
            invalid_email = True
            invalid_registration = True
            
        try:
            confirm_email = request.POST["confirmEmail"]
        except KeyError:
            confirm_email = ""
            invalid_confirm_email = True
            invalid_registration = True
            
        try:
            password = request.POST["password"]
        except KeyError:
            password = ""
            invalid_password = True
            invalid_registration = True
            
        try:
            confirm_password = request.POST["confirmPassword"]
        except KeyError:
            confirm_password = ""
            invalid_confirm_password = True
            invalid_registration = True
        
        try:
            month = request.POST["month"]
        except KeyError:
            month = ""
            invalid_month = True
            invalid_registration = True
        
        try:
            day = request.POST["day"]
        except KeyError:
            day = ""
            invalid_day = True
            invalid_registration = True
        
        try:
            year = request.POST["year"]
        except KeyError:
            year = ""
            invalid_year = True
            invalid_registration = True
            
        try:
            gender = request.POST["gender"]
        except KeyError:
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
        except Member.DoesNotExist:
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
    except Member.DoesNotExist:
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
    except KeyError:
        pass

    return HttpResponseRedirect("/login/")
