from django.contrib import admin
from .models import Category, Brand, Product, ProductAttribute

admin.site.register(Category)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', ) #, 'image_tag'


admin.site.register(Brand, BrandAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','category', 'brand', 'status', 'is_featured')
    list_editable = ('status', 'is_featured')


admin.site.register(Product, ProductAdmin)


# Product Attribute
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'price', 'image_tag')


admin.site.register(ProductAttribute, ProductAttributeAdmin)


