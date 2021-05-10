from .models import Category, Brand


def get_filters(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    context = {
        'categories': categories,
        'brands': brands,
    }
    return context
