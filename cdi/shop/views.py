from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string

from .models import Category, Brand, Product


def home(request):
    products = Product.objects.all()
    feat_products = products.filter(is_featured=True)
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Shop',
        'feat_products': feat_products,
        'page_obj': page_obj
    }
    return render(request, 'shop/home.html', context)


def product_detail(request, slug, _id):
    queryset = Product.objects.get(id=_id)
    related_products = Product.objects.filter(category=queryset.category).exclude(id=_id)[:4]
    # exclude(id=id) :Exclude the current product
    context = {
        'title': 'Product Detail',
        'data': queryset,
        'related_products': related_products,
    }
    return render(request, 'shop/product-detail.html', context)


def search(request):
    q = request.GET['q']
    products = Product.objects.filter(name__icontains=q)
    total_data = products.count()
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_data': total_data
    }
    return render(request, 'shop/search.html', context)


# Filter data
def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    all_products = Product.objects.all().distinct()
    if len(categories) > 0:
        all_products = all_products.filter(category_id__in=categories).distinct()
    if len(brands) > 0:
        all_products = all_products.filter(brand__id__in=brands).distinct()
    t = render_to_string('shop/ajax/product-list.html', {'data': all_products})
    return JsonResponse({'data': t})
