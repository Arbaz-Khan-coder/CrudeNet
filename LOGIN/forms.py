from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from BLOG.models import MediaPost_Video,MediaPost_Image,Comment

#REGISTRATION FORM
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username","email","password1","password2"]

# UPDATE USERNAME & EMAIL
class UserUpdateForm(ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username","email"]


#UPDATE PROFILE
class UserDPForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["dp"]

# UPLOAD VIDEO
class VideoForm(ModelForm):
    class Meta:
        model= MediaPost_Video
        fields= ["caption", "video"]
        widgets = {
            'caption' : forms.Textarea(attrs={
                'rows': '3',
                'cols': '20',
                'maxlength': '100',
            }),
        }

# UPLOADING IMAGE
class ImageForm(ModelForm):
    class Meta:
        model = MediaPost_Image
        fields = ["caption", "image"]
        widgets = {
            'caption' : forms.Textarea(attrs={
                'rows': '3',
                'cols': '20',
                'maxlength': '100',
            }),
        }

class CommentForm(forms.ModelForm): 
    class Meta: 
        model = Comment
        fields =['comments']
        widgets = {
            'comments' : forms.Textarea(attrs={
                'rows': '3',
                'cols': '20',
                'maxlength': '300',
            }),
        }