from django.db import models
from main.models import Section


class BlogModel(models.Model):
    blog_title = models.CharField(max_length=100)
    section = models.ForeignKey(
        Section, related_name='blogs', on_delete=models.CASCADE)
    blog = models.TextField()
    image = models.ImageField(blank=True, upload_to='images')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_on = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-timestamp', )
        verbose_name_plural = '1. BlogModels'

    def __str__(self):
        return self.blog_title


class CommentModel(models.Model):
    your_name = models.CharField(max_length=100)
    your_email = models.EmailField(max_length=254)
    comment_text = models.TextField()
    blog = models.ForeignKey('BlogModel', on_delete=models.CASCADE, related_name='commented_blog')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp', )
        verbose_name_plural = '2. CommentModels'

    def __str__(self):
        return f'Comment by Name: {self.your_name}'
