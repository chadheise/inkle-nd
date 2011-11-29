from django import forms
from django.forms import ModelForm
from models import GENDERS

class login_form(forms.Form):
    email = forms.CharField(max_length = 20, label = "Email", widget = forms.TextInput)
    password = forms.CharField(max_length = 20, label = "Password", widget = forms.PasswordInput)

class registration_form(forms.Form):
    first_name = forms.CharField(max_length = 20, label = "First name", widget = forms.TextInput)
    last_name = forms.CharField(max_length = 20, label = "Last name", widget = forms.TextInput)
    email = forms.CharField(max_length = 20, label = "Email", widget = forms.TextInput)
    email_verify = forms.CharField(max_length = 20, label = "Re-enter email", widget = forms.TextInput)
    password = forms.CharField(max_length = 20, label = "Password", widget = forms.PasswordInput)
    gender = forms.ChoiceField(choices = GENDERS, label = "Gender", widget = forms.Select(attrs = {}))

#class recipe_form(forms.Form):
#    category = forms.ChoiceField(choices=categories, label="Category", widget=forms.Select(attrs={}))
#    title = forms.CharField(max_length=50)
#    preparation = forms.CharField(max_length=5000, widget=forms.widgets.Textarea(), required=False)
#    serving = forms.CharField(max_length=5000, widget=forms.widgets.Textarea(), required=False)
#    notes = forms.CharField(max_length=5000, widget=forms.widgets.Textarea(), required=False)
#    #card = forms.ImageField(required=False)
