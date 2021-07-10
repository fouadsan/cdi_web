from django.contrib import admin
from .models import Category, Brand, Product, ProductAttribute, CartOrder, CartOrderItems, ProductReview

admin.site.register(Category)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )  # , 'image_tag'


admin.site.register(Brand, BrandAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'brand', 'status', 'is_featured')
    list_editable = ('status', 'is_featured')


admin.site.register(Product, ProductAdmin)


# Product Attribute
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'price', 'image_tag')


admin.site.register(ProductAttribute, ProductAttributeAdmin)


# Order
class CartOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amt', 'paid_status', 'order_dt')


admin.site.register(CartOrder, CartOrderAdmin)


# OrderItems
class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'item',
                    'image_tag', 'qty', 'price', 'total')


admin.site.register(CartOrderItems, CartOrderItemsAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'review_text', 'get_review_rating')


admin.site.register(ProductReview, ProductReviewAdmin)
