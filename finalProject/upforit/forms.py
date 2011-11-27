from django import forms
from django.forms import ModelForm
#from models import categories

class login_form(forms.Form):
    email = forms.CharField(max_length = 20, label = "Email", widget = forms.TextInput)
    password = forms.CharField(max_length = 20,label = "Password", widget = forms.PasswordInput)

#class register_form(login_form):
#    email = forms.CharField(max_length = 20, label = "Email", widget = forms.TextInput)

#class recipe_form(forms.Form):
#    category = forms.ChoiceField(choices=categories, label="Category", widget=forms.Select(attrs={}))
#    title = forms.CharField(max_length=50)
#    preparation = forms.CharField(max_length=5000, widget=forms.widgets.Textarea(), required=False)
#    serving = forms.CharField(max_length=5000, widget=forms.widgets.Textarea(), required=False)
#    notes = forms.CharField(max_length=5000, widget=forms.widgets.Textarea(), required=False)
#    #card = forms.ImageField(required=False)
