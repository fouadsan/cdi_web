from django.db import models
from django.contrib import admin


class Section(models.Model):
    name = models.CharField(max_length=150, db_index=True, unique=True)
    description = models.TextField()
    image_one = models.ImageField(upload_to='images')  # Important!!!!!!
    image_two = models.ImageField(upload_to='images')  # Important!!!!!!
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created_at', )
        verbose_name = 'section'
        verbose_name_plural = 'sections'


class Team(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True)
    occupation = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images')

    def __str__(self):
        return self.name


class Contact(models.Model):
    content = models.TextField()

    def __str__(self):
        return f"Contact"
