from django.urls import path

from .views import home, signup
from shop.views import add_to_cart

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('add-to-cart', add_to_cart, name='add_to_cart'),
    path('accounts/signup', signup, name='signup'),
]
