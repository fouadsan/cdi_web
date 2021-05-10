from django.contrib import admin
from django.urls import path
from .views import home, product_detail, search, filter_data

app_name = 'shop'

urlpatterns = [
    path('', home, name='home'),
    path('<str:slug>/<int:_id>', product_detail, name='product-detail'),
    path('search', search, name='search'),
    path('filter-data', filter_data, name='filter_data'),
]
