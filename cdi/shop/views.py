import calendar
from django.contrib.auth import login
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.db.models import Max, Min, Avg, Count
from django.db.models.functions import ExtractMonth
from .models import Category, Brand, Product, ProductAttribute, CartOrder, CartOrderItems, ProductReview, Wishlist, UserAddressBook
from django.contrib.auth.decorators import login_required
from .forms import ReviewAdd, AddressBookForm

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

    reviewForm = ReviewAdd()

    canAdd = True
    reviewCheck = ProductReview.objects.filter(
        user=request.user, product=queryset).count()
    if request.user.is_authenticated:
        if reviewCheck > 0:
            canAdd = False

    reviews = ProductReview.objects.filter(product=queryset)

    # Fetch avg rating for reviews
    avg_reviews = ProductReview.objects.filter(
        product=queryset).aggregate(avg_rating=Avg('review_rating'))
    # End

    context = {
        'title': queryset.name,
        'data': queryset,
        'related_products': related_products,
        'form': reviewForm,
        'canAdd': canAdd,
        'reviews': reviews,
        'avg_reviews': avg_reviews

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

    total_amt = 0
    totalAmt = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            totalAmt += int(item['qty']) * float(item['price'])
        # Order
        order = CartOrder.objects.create(
            user=request.user,
            total_amt=totalAmt,
        )
        # End
        for p_id, item in request.session['cartdata'].items():
            total_amt += int(item['qty']) * float(item['price'])
            # OrderItems
            items = CartOrderItems.objects.create(
                order=order,
                invoice_no='INV-' + str(order.id),
                item=item['name'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty']) * float(item['price'])
            )
            # End
            host = request.get_host()
            paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': total_amt,
                'item_name': 'OrderNo-' + str(order.id),
                'invoice': 'INV-' + str(order.id),
                'currency_code': 'USD',
                'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
                'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
                'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
            }
            form = PayPalPaymentsForm(initial=paypal_dict)
            address = UserAddressBook.objects.filter(
                user=request.user, status=True).first()
        context = {
            'title': 'Shopping Cart',
            'cart_data': request.session['cartdata'],
            'totalitems': len(request.session['cartdata']),
            'total_amt': total_amt,
            'form': form,
            'address': address
        }
        return render(request, 'shop/checkout.html', context)


@csrf_exempt
def payment_done(request):
    returnData = request.POST
    return render(request, 'shop/payment-success.html', {'data': returnData})


@csrf_exempt
def payment_cancelled(request):
    return render(request, 'shop/payment-fail.html')


# Save Review
def save_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    review = ProductReview.objects.create(
        user=user,
        product=product,
        review_text=request.POST['review_text'],
        review_rating=request.POST['review_rating'],
    )
    data = {
        'user': user.username,
        'review_text': request.POST['review_text'],
        'review_rating': request.POST['review_rating']
    }

    # Fetch avg rating for reviews
    avg_reviews = ProductReview.objects.filter(
        product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    context = {
        'bool': True,
        'data': data,
        'avg_reviews': avg_reviews
    }

    return JsonResponse(context)


# User Dashboard


def my_dashboard(request):
    orders = CartOrder.objects.annotate(month=ExtractMonth('order_dt')).values(
        'month').annotate(count=Count('id')).values('month', 'count')

    month_number = []
    total_orders = []
    for d in orders:
        month_number.append(calendar.month_name[d['month']])
        total_orders.append(d['count'])

    context = {
        'month_number': month_number,
        'total_orders': total_orders
    }
    return render(request, 'shop/user/dashboard.html', context)


# My Orders
def my_orders(request):
    orders = CartOrder.objects.filter(user=request.user).order_by('-id')
    return render(request, 'shop/user/orders.html', {'orders': orders})


# Order Detail
def my_order_items(request, id):
    order = CartOrder.objects.get(pk=id)
    orderitems = CartOrderItems.objects.filter(order=order).order_by('-id')
    return render(request, 'shop/user/order-items.html', {'orderitems': orderitems})


def add_wishlist(request):
    pid = request.GET['product']
    product = Product.objects.get(pk=pid)
    data = {}
    checkw = Wishlist.objects.filter(
        product=product,
        user=request.user).count()
    if checkw > 0:
        data = {
            'bool': False
        }
    else:
        wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )
        data = {
            'bool': True
        }
    return JsonResponse(data)


# My Wishlist
def my_wishlist(request):
    wlist = Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request, 'shop/user/wishlist.html', {'wlist': wlist})


# My Reviews
def my_reviews(request):
    reviews = ProductReview.objects.filter(user=request.user).order_by('-id')
    return render(request, 'shop/user/reviews.html', {'reviews': reviews})


# My Addressbook
def my_addressbook(request):
    addbook = UserAddressBook.objects.filter(user=request.user).order_by('-id')
    return render(request, 'shop/user/addressbook.html', {'addbook': addbook})


# Save AddressBook
def save_address(request):
    msg = None
    if request.method == 'POST':
        form = AddressBookForm(request.POST)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                UserAddressBook.objects.update(status=False)
            saveForm.save()
            msg = 'Data has been saved'
    form = AddressBookForm
    context = {
        'msg': msg,
        'form': form
    }
    return render(request, 'shop/user/add-address.html', context)


# Activate Address
def activate_address(request):
    a_id = str(request.GET['id'])
    UserAddressBook.objects.update(status=False)
    UserAddressBook.objects.filter(id=a_id).update(status=True)

    return JsonResponse({'bool': True})


# Update AddressBook
def update_address(request, id):
    address = UserAddressBook.objects.get(pk=id)
    msg = None
    if request.method == 'POST':
        form = AddressBookForm(request.POST, instance=address)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                UserAddressBook.objects.update(status=False)
            saveForm.save()
            msg = 'Data has been saved'
    form = AddressBookForm(instance=address)
    context = {
        'msg': msg,
        'form': form
    }
    return render(request, 'shop/user/update-address.html', context)
