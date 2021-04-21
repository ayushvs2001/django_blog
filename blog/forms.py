from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class PostForm(forms.ModelForm):

    class Meta():
        model = Post   # model we have to link
        fields = ('title', 'text') # field we have to change or update

        widgets = {
            'title': forms.TextInput(attrs={"style":'width:800px; height:50px; padding-bottom:30px; margin-bottom: 30px;'}),
            'text': forms.Textarea(attrs={"style":'width:800px; height:350px;'})
        }


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('text', )

        widgets = {
           'text': forms.Textarea(attrs={"style":'width:700px; height:150px;'})
        }



class UserRegistrationForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['username', 'email', 'password1', 'password2']
