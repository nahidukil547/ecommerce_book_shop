from django.urls import path
from . import views
from . import views_payment

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),

    path('product=details/<slug:product_slug>/', views.product_details, name='product_details'),
    path('add-or-update-cart/', views.add_or_update_cart, name='add_or_update_cart'),
    path('cart-details/', views.cart_details, name='cart_details'),
    path('checkout/', views.checkout, name='checkout'),

    path('payment/success/<str:str_data>/', views_payment.payment_complete, name='payment_complete'),
    path('payment/cancel/<str:str_data>/', views_payment.payment_cancel, name='payment_cancel'),
    path('payment/fail/<str:str_data>/', views_payment.payment_failed, name='payment_failed'),
    path('payment/check/<str:str_data>/', views_payment.payment_check, name="payment_check"),
]

