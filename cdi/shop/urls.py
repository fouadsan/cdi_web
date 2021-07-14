from django.contrib import admin
from django.urls import path, include


from .views import add_wishlist, home, product_detail, search, filter_data,\
    load_more_data, cart_list, delete_cart_item, update_cart_item, checkout, save_review, my_dashboard, my_orders, my_order_items,\
    add_wishlist, my_wishlist, my_reviews, my_addressbook, save_address, activate_address

app_name = 'shop'

urlpatterns = [
    path('', home, name='home'),
    path('<str:slug>/<int:_id>/', product_detail, name='product-detail'),
    path('search', search, name='search'),
    path('filter-data', filter_data, name='filter_data'),
    path('load-more-data', load_more_data, name='load_more_data'),
    path('cart', cart_list, name='cart'),
    path('delete-from-cart', delete_cart_item, name='delete_from_cart'),
    path('update-cart', update_cart_item, name='update_cart'),
    path('checkout', checkout, name='checkout'),
    path('save-review/<int:pid>', save_review, name='save_review'),
    # User Section Start
    path('my-dashboard', my_dashboard, name='my_dashboard'),
    path('my-orders', my_orders, name='my_orders'),
    path('my-order-items/<int:id>', my_order_items, name='my_order_items'),
    # End
    # Wishlist
    path('wishlist', add_wishlist, name='wishlist'),
    path('my-wishlist', my_wishlist, name='my_wishlist'),
    # My Reviews
    path('my-reviews', my_reviews, name='my_reviews'),
    # My AddressBook
    path('my-addressbook', my_addressbook, name='my_addressbook'),
    path('add-address', save_address, name='add_address'),
    path('activate-address', activate_address, name='activate_address'),



]
