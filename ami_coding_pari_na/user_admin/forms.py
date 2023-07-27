from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


USER_TYPE= [
    ('student', 'Student'),
    ('teacher', 'Teacher')
    ]


class createuserform(forms.ModelForm):
    class Meta:
        model = User
        fields = ('f_name', 'l_name','email', 'password')
        labels = {'f_name':'First Name', 'l_name':'Last Name','email':'Email', 'password':'Password'}

        widgets = {
            'f_name' : forms.TextInput(attrs={'class':'form-control'}),
            'l_name' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.TextInput(attrs={'class':'form-control', 'type':'email', 'autocomplete':'off'}),
            'password' : forms.TextInput(attrs={'class':'form-control', 'type':'password'}),
        }


class Permissionform(forms.ModelForm):
    class Meta:
        model = User
        fields = ('active',)
        widgets = {
            'f_name' : forms.TextInput(attrs={'class':'form-control'}),
            'l_name' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.TextInput(attrs={'class':'form-control', 'type':'email', 'autocomplete':'off'})
        }