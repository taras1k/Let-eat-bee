from django import forms
from models import *


class RegisterForm(forms.Form):
    user_name = forms.CharField(max_length=100)
    user_password = forms.CharField(max_length=100)
    user_password_check = forms.CharField(max_length=100)
    user_mail = forms.EmailField()
    user_first_name = forms.CharField(max_length=100)
    user_last_name = forms.CharField(max_length=100)
    
    def clean_user_name(self):
        data = self.cleaned_data
        try:
             User.objects.get( username = data['user_name'])
        except User.DoesNotExist:
            return data['user_name']
        raise forms.ValidationError('This user name is already taken.') 
        
    def clean_user_mail(self):
        data = self.cleaned_data
        try:
             User.objects.get( email = data['user_mail'])
        except User.DoesNotExist:
            return data['user_mail']
        raise forms.ValidationError('This mail is already taken.') 

    def clean_user_password_check(self):
        data = self.cleaned_data
        if data['user_password_check'] == data['user_password']:
            return data['user_password_check']
        raise forms.ValidationError('Password missmatch.') 

    
class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=100)
    user_password = forms.CharField(max_length=100)


