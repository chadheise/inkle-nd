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
                                 "",
                                 {},
                                 context_instance = RequestContext(request)
                             )

def people_view(request):
    # If a user is not logged in, redirect them to the login page
    if ("member_id" not in request.session):
           return HttpResponseRedirect("/upforit/login")
    
    # Get the member who is logged in
    member = Member.objects.get(pk = request.session["member_id"])

    members = Member.objects.all()
    return render_to_response(
                                 "people.html",
                                 {
                                     "member" : member,
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
            except:
                return HttpResponseRedirect("/upforit/") #TODO: why go back to home?

            # If the member's credentials are correct, log them in and return them to the home page
            if (member.password == log_form.cleaned_data["password"]):
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

def register_view(request):    
    """New user registration."""
    # If the POST data is empty, return an empty form
    if (not request.POST):
        form = registration_form()
        member = None

    # If the user has submitted valid POST data, create a new user and send the user to the login page
    else:
        form = registration_form(request.POST)
        if (form.is_valid()):
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            email_verify = form.cleaned_data["email_verify"]
            password = form.cleaned_data["password"]
            gender = form.cleaned_data["gender"]

            if (email == email_verify):
                member = Member(
                    first_name = first_name,
                    last_name = last_name,
                    username = email,
                    password = password,
                    email = email,
                    gender = gender,
                    phone = "7175670234"
                )
                member.is_staff = True
                member.save()
                return HttpResponseRedirect("/upforit/login")

    return render_to_response(
                                 "register.html",
                                 {
                                     "form" : form
                                 },
                                 context_instance=RequestContext(request)
                             )

def logout_view(request):
    """Logs out the current user."""
    if (request.session["member_id"]):
        del request.session["member_id"]
    
    return HttpResponseRedirect("/upforit/login")
