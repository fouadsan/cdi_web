from django import forms
from django.db import models
from django.forms import fields

from .models import ProductReview, UserAddressBook


# Review Add Form
class ReviewAdd(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ('review_text', 'review_rating')


# AddressBook Add Form
class AddressBookForm(forms.ModelForm):
    class Meta:
        model = UserAddressBook
        fields = ('address', 'mobile', 'status')
