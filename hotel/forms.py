from django import forms
from django.db.models import fields
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from phonenumber_field.modelfields import PhoneNumberField
from .models import Booking, User, Room

class NewUserForm(UserCreationForm):
    username = forms.CharField(
        label=_('User Name'),
        required=True,
    )
    first_name = forms.CharField(
        label=_('First Name'),
        required=True,
    )
    last_name = forms.CharField(
        label=_('Last Name'),
        required=True,
    )
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput,
        required=True,
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        required=True
    )
    password2 = forms.CharField(
        label=_('Conrfirm Password'),
        widget=forms.PasswordInput,
        required=True
    )
    phoneNumber = PhoneNumberField()
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phoneNumber', 'password1', 'password2')
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(_("Username is already in use."))
        return username
    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'phoneNumber')

class EditRoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ["capacity", "numberOfBeds", "room_price", "roomType"]
