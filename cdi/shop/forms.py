from django import forms
from django.db import models
from django.forms import fields

from .models import ProductReview


class ReviewAdd(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ('review_text', 'review_rating')
