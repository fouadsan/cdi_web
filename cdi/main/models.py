from django.db import models
from django.utils.html import mark_safe


class Banner(models.Model):
    image = models.ImageField(upload_to="images/banner_images")
    alt_text = models.CharField(max_length=100)

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Banner'
        verbose_name_plural = '1. Banners'

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % self.image.url)

    def __str__(self):
        return self.alt_text


class Section(models.Model):
    name = models.CharField(max_length=150, db_index=True, unique=True)
    description = models.TextField()
    icon_class = models.CharField(max_length=150, blank=True)
    # image_one = models.ImageField(upload_to='images')  # Important!!!!!!
    # image_two = models.ImageField(upload_to='images')  # Important!!!!!!
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at', )
        verbose_name = 'Section'
        verbose_name_plural = '2. Sections'

    def __str__(self):
        return self.name


class Teammate(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True)
    occupation = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images')

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Teammate'
        verbose_name_plural = '3. Teammates'

    def __str__(self):
        return self.name


class Contact(models.Model):
    content = models.TextField()

    def __str__(self):
        return f"Contact"
