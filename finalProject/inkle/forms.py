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
    email_confirm = forms.CharField(max_length = 20, label = "Confirm email", widget = forms.TextInput)
    password = forms.CharField(max_length = 20, label = "Password", widget = forms.PasswordInput)
    password_confirm = forms.CharField(max_length = 20, label = "Confirm password", widget = forms.TextInput)
    gender = forms.ChoiceField(choices = GENDERS, label = "Gender", widget = forms.Select(attrs = {}))

