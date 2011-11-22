from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404

from django.shortcuts import render_to_response

from django.contrib.auth.models import User
from django.contrib import auth

from finalProject.upforit.models import *
from finalProject.upforit.forms import *

import datetime

def upforit_view(request):
    if "member_id" not in request.session:  #Check if user is not logged in
           return HttpResponseRedirect('/upforit/login') #Redirect to login page
    uid = request.session['member_id']
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
    #test_recipe = test_recipe[0]
    
    return render_to_response('upforit.html', locals(), context_instance=RequestContext(request))

def login_view(request):
    if "member_id" in request.session: #If they have previously logged in
        return HttpResponseRedirect('/upforit')  #Take them to main page
    if request.POST:
        form = login_form(request.POST)
        if form.is_valid():
            try:
                m = User.objects.get(username=form.cleaned_data['username'])
            except:
                return HttpResponseRedirect('/upforit/')
            if m.check_password(form.cleaned_data['password']):
                request.session['member_id'] = m.id
                return HttpResponseRedirect('/upforit/')
            else:
                return render_to_response('login.html', {'form':form}, context_instance=RequestContext(request))
    else: # request.POST is empty
        form = login_form()
    return render_to_response('login.html', {'form':form}, context_instance=RequestContext(request))

def register_view(request):    
    if request.POST:
        form = register_form(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
                email = form.cleaned_data['email'])
            user.save()
            return HttpResponseRedirect('/upforit/login')
    else: # request.POST is empty
        form = register_form()
    return render_to_response('register.html', {'form':form}, context_instance=RequestContext(request))

def logout_view(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return render_to_response('logout.html', locals(), context_instance=RequestContext(request))
