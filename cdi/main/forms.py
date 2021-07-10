from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ContactUs(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)


class SignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=50, required=True)
    mobile = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'number'}), required=True)
    address = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ('full_name', 'mobile', 'address',
                  'username', 'password1', 'password2')
