from .models import Category, Brand, ProductAttribute, Product
from django.db.models import Min, Max
from .utils import store_open


def get_filters(request):
    is_open = store_open()
    products = Product.objects.all()  # NEW
    categories = Category.objects.all()
    brands = Brand.objects.all()
    min_max_price = ProductAttribute.objects.aggregate(
        Min('price'), Max('price'))
    context = {
        'is_open': is_open,
        'products': products,  # NEW
        'categories': categories,
        'brands': brands,
        'min_max_price': min_max_price
    }
    return context
