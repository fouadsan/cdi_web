from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Category'
        verbose_name_plural = '1. Categories'

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=150, db_index=True, unique=True)
    image = models.ImageField(blank=True, null=True,
                              upload_to='images/brand_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Brand'
        verbose_name_plural = '2. Brands'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.image.url)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=False)
    slug = models.CharField(max_length=400)
    description = models.TextField(max_length=800)
    specs = models.TextField(max_length=800)
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE, blank=True, null=True)
    brand = models.ForeignKey(
        Brand, related_name='products', on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at', )
        verbose_name_plural = '3. Products'


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(blank=True, null=True)
    image_url1 = models.URLField(null=True)
    image_url2 = models.URLField(blank=True)
    image_url3 = models.URLField(blank=True)
    image_url4 = models.URLField(blank=True)

    class Meta:
        ordering = ('-id', )
        verbose_name_plural = '4. ProductsAttributes'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.image_url1)

    def __str__(self):
        return self.product.name


# Order
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amt = models.FloatField()
    paid_status = models.BooleanField(default=False)
    order_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '8. Orders'


# Order Items
class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=150)
    item = models.CharField(max_length=150)
    image = models.CharField(max_length=200)
    qty = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()

    class Meta:
        verbose_name_plural = '9. Order Items'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % self.image)
