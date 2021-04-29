from django.contrib import admin
from django.urls import path
from .views import blog_list_view, blog_detail_view

app_name = 'blog'

urlpatterns = [
    path('', blog_list_view, name='blogs'),
    path('<int:_id>', blog_detail_view, name='blog-detail'),
]