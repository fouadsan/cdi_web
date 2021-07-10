from django.contrib.auth import login
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.db.models import Max, Min
from .models import Category, Brand, Product, ProductAttribute
from django.contrib.auth.decorators import login_required

# paypal
from django.conf import settings

from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm


def home(request):
    products = Product.objects.all()[:3]
    total_data = Product.objects.count()
    min_price = ProductAttribute.objects.aggregate(Min('price'))
    max_price = ProductAttribute.objects.aggregate(Max('price'))
    feat_products = Product.objects.filter(is_featured=True)
    # paginator = Paginator(products, 9)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Shop',
        'feat_products': feat_products,
        'products': products,
        'total_data': total_data,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'shop/home.html', context)


def product_detail(request, slug, _id):
    queryset = Product.objects.get(id=_id)
    related_products = Product.objects.filter(
        category=queryset.category).exclude(id=_id)[:4]
    # exclude(id=id) :Exclude the current product
    context = {
        'title': queryset.name,
        'data': queryset,
        'related_products': related_products,
    }
    return render(request, 'shop/product-detail.html', context)


def search(request):
    q = request.GET['q']
    products = Product.objects.filter(name__icontains=q)
    total_data = products.count()
    # paginator = Paginator(products, 6)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    context = {
        'products': products,
        'total_data': total_data
    }
    return render(request, 'shop/search.html', context)


# Filter data
def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    min_price = request.GET['minPrice']
    max_price = request.GET['maxPrice']
    all_products = Product.objects.all().distinct()
    all_products = all_products.filter(productattribute__price__gte=min_price)
    all_products = all_products.filter(productattribute__price__lte=max_price)
    if len(categories) > 0:
        all_products = all_products.filter(
            category_id__in=categories).distinct()
    if len(brands) > 0:
        all_products = all_products.filter(brand_id__in=brands).distinct()
    t = render_to_string('shop/ajax/product-list.html', {'data': all_products})
    return JsonResponse({'data': t})


# Load More
def load_more_data(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = Product.objects.all().order_by('-id')[offset:offset + limit]
    t = render_to_string('shop/ajax/product-list.html', {'data': data})
    return JsonResponse({'data': t})


# Add to cart
def add_to_cart(request):
    # del request.session['cartdata']
    cart_p = {str(request.GET['id']): {
        'image': request.GET['image'],
        'name': request.GET['name'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
    }}
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = int(
                cart_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = cart_p
    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})


# Cart List Page
def cart_list(request):
    total_amt = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            total_amt += int(item['qty']) * float(item['price'])
        context = {
            'title': 'Shopping Cart',
            'cart_data': request.session['cartdata'],
            'totalitems': len(request.session['cartdata']),
            'total_amt': total_amt
        }
        return render(request, 'shop/cart.html', context)

    else:
        context = {
            'title': 'Shopping Cart',
            'cart_data': '',
            'totalitems': 0,
            'total_amt': total_amt
        }
    return render(request, 'shop/cart.html', context)


# Delete Cart Item
def delete_cart_item(request):
    p_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata'] = cart_data
    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty']) * float(item['price'])
    t = render_to_string('shop/ajax/cart-list.html', {'cart_data': request.session['cartdata'],
                                                      'totalitems': len(request.session['cartdata']),
                                                      'total_amt': total_amt})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})


# Update Cart Item
def update_cart_item(request):
    p_id = str(request.GET['id'])
    p_qty = request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = p_qty
            request.session['cartdata'] = cart_data
    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty'])*float(item['price'])
    t = render_to_string('shop/ajax/cart-list.html', {'cart_data': request.session['cartdata'],
                                                      'totalitems': len(request.session['cartdata']), 'total_amt': total_amt})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})


# Checkout
@login_required
def checkout(request):
    # Process Payment
    order_id = '123'
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '123',
        'item_name': 'Item Name',
        'invoice': 'INV-123',
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    total_amt = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            total_amt += int(item['qty']) * float(item['price'])
        context = {
            'title': 'Shopping Cart',
            'cart_data': request.session['cartdata'],
            'totalitems': len(request.session['cartdata']),
            'total_amt': total_amt,
            'form': form
        }
        return render(request, 'shop/checkout.html', context)


@csrf_exempt
def payment_done(request):
    returnData = request.POST
    return render(request, 'shoppayment-success.html', {'data': returnData})


@csrf_exempt
def payment_cancelled(request):
    return render(request, 'shop/payment-fail.html')
