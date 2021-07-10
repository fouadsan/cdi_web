from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from shop.views import payment_cancelled, payment_done

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('blogs/', include('blog.urls')),
    path('shop/', include('shop.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-done/', payment_done, name='payment_done'),
    path('payment-cancelled/', payment_cancelled, name='payment_cancelled'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
