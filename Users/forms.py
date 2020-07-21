from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import JSProfile




class UserUpdateForm(forms.ModelForm):
	email=forms.EmailField(required=False)
	
	class Meta:
		model = User
		fields = ['email']

class ProfileUpdateForm(forms.ModelForm):
	
	class Meta:
		model = JSProfile
		fields = ['img','Resume','BirthDate','phoneno']

class UserPwdForm(PasswordChangeForm):
	class Meta:
		model = User
		fields=['username','password1','password2']