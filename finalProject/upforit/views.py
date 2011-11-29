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
    if "member_id" not in request.session:
           return HttpResponseRedirect("/upforit/login")

    locations = Location.objects.all()
    
    """uid = request.session['member_id']
    user = User.objects.get(pk=uid)
    category_names = [c[1] for c in categories]
    ingredient_dict = {}
    #for rec in Recipe.objects.all():
    #    ingredient_dict[rec] = Ingredient.objects.filter(recipe=rec)
    ingredients = Ingredient.objects.all()
    
    recipe_dict = {}
    for cat in category_names:
        recipe_dict[cat] = Recipe.objects.filter(category=cat)
        
    if request.POST:
        new_recipe_form = recipe_form(request.POST, request.FILES)
        new_ingredient_forms = []
        
        #---------Edit recipe if edit was submitted--------------#
        if 'edit_recipe_value' in request.POST:
            recipeID = request.POST['edit_recipe_value']
        else:
            recipeID = "-1"
        if (recipeID != "-1"):
            recipe = Recipe.objects.get(pk=recipeID)
            recipe.preparation = request.POST['edit_preparation'+recipeID] 
            recipe.serving = request.POST['edit_serving'+recipeID]
            recipe.notes = request.POST['edit_notes'+recipeID]
            recipe.update = datetime.datetime.now()
            recipe.save()
            ingredient_list = Ingredient.objects.filter(recipe=recipe) #Get all ingredients for this recipe
            for ingr in ingredient_list: #update all ingredients with changes
                ingr.quantity = request.POST['edit_ingredient_qty'+str(ingr.id)]
                ingr.measurement_type = request.POST['edit_ingredient_measurement'+str(ingr.id)]
                ingr.item = request.POST['edit_ingredient_item'+str(ingr.id)]
                ingr.save()
        #---------Delete recipe if delete was submitted--------------#
        if 'delete_recipe_value' in request.POST:
            deleteID = request.POST['delete_recipe_value']
        else:
            deleteID = "-1"
        if (deleteID != "-1"):
            recipe = Recipe.objects.get(pk=deleteID)
            ingredient_list = Ingredient.objects.filter(recipe=recipe) #Get all ingredients for this recipe
            for ingr in ingredient_list:
                ingr.delete() #Delete all ingredients for this recipe
            recipe.delete()
        #---------Create recipe if new recipe was submitted--------------#
        if new_recipe_form.is_valid():
            recipe = Recipe.objects.create(category=new_recipe_form.cleaned_data['category'],
                title = new_recipe_form.cleaned_data['title'],
                preparation = new_recipe_form.cleaned_data['preparation'],
                serving = new_recipe_form.cleaned_data['serving'],
                notes = new_recipe_form.cleaned_data['notes'],
                creator = user,
                update = datetime.datetime.now())
                #card = request.FILES['card'])
            recipe.save()
            for i in range(1, int(request.POST['num_ingredients'])+1): #loop over all ingredient forms
                ingredient = Ingredient.objects.create(item = request.POST['item'+str(i)],
                    quantity = request.POST['qty'+str(i)],
                    measurement_type = request.POST['measurement'+str(i)],
                    recipe = recipe)
                ingredient.save()
    else: # request.POST is empty
        new_recipe_form = recipe_form()
    
    #print Recipe.objects.all()
    #print new_recipe_form.cleaned_data['card']
    #print recipe.card
    #print request.FILES
    #test_recipe = Recipe.objects.all()
    #test_recipe = test_recipe[0]"""
    
    return render_to_response(
                                 "upforit.html",
                                 locals(),
                                 context_instance = RequestContext(request)
                             )

def location_view(request, location_id = None):
    # Get the member who is logged in
    member = User.objects.get(pk = request.session["member_id"])
    
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

def edit_location_view2(request, location_id, name, street, city, state, zip_code, category):
    sphere = Sphere(name = "S1")
    sphere.save()    

    # Get the member who is logged in
    member = User.objects.get(pk = request.session["member_id"])
    
    # If the location ID is invalid, throw a 404 error
    try:
        location = Location.objects.get(pk = int(location_id))
    except:
        raise Http404()

    location.name = name
    location.street = street
    location.city = city
    location.state = state
    location.zip_code = int(zip_code)
    location.category = category

    location.save()
    
    return render_to_response(
                                 "upforit.html",
                                 {},
                                 context_instance = RequestContext(request)
                             )

def edit_location_view(request, location_id = None):
    # Get the member who is logged in
    member = User.objects.get(pk = request.session["member_id"])
    
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

def login_view(request):
    """User login."""
    # If a user is already logged in, go to the main page
    if "member_id" in request.session:
        return HttpResponseRedirect("/upforit")
    
    # If the POST data is empty, return an empty form
    if (not request.POST):
        form = login_form()
    
    # If the user has submitted POST data, see if the information is valid
    else:
        form = login_form(request.POST)
        if form.is_valid():
            # Check if a member with the given username already exists
            try:
                member = User.objects.get(username = form.cleaned_data["email"])
            except:
                return HttpResponseRedirect("/upforit/") #TODO: why go back to home?

            # If the member's credentials are correct, log them in and return them to the home page
            if member.check_password(form.cleaned_data["password"]):
                request.session["member_id"] = member.id
                return HttpResponseRedirect("/upforit/")
    
    return render_to_response(
                                 "login.html",
                                 {
                                     "form" : form
                                 },
                                 context_instance=RequestContext(request)
                             )

def register_view(request):    
    """New user registration."""
    # If the POST data is empty, return an empty form
    if (not request.POST):
        form = login_form()

    # If the user has submitted valid POST data, create a new user and send the user to the login page
    else:
        form = login_form(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data["email"],
                password = form.cleaned_data["password"],
                email = form.cleaned_data["email"]
            )
            user.is_staff = True
            user.save()
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

    return render_to_response(
                                 "logout.html",
                                 {},
                                 context_instance = RequestContext(request)
                             )
