from django import forms
from django.contrib.auth import get_user_model

from .models import Profile

# User model
User = get_user_model()


# ****** Update user's username and email Form ******
class UserUpdateForm(forms.ModelForm):

    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        max_length=20,
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs={'placeholder': 'Email'}),
        max_length=255,
    )

    class Meta:
        model = User
        fields = ['username', 'email', ]


# ****** Update user's profile Form ******
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', ]
