from django.urls import path
from . import views
from . import views_payment

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),

    path('authors/', views.author_list, name='author_list'),
    path('author=details/<slug:author_slug>/', views.author_details, name='author_details'),

    path('products/', views.products_list, name='products_list'),
    path('product=details/<slug:product_slug>/', views.product_details, name='product_details'),


    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),

    path('products/search/', views.products_search, name='products_search'),



    path('add-or-update-cart/', views.add_or_update_cart, name='add_or_update_cart'),
    path('cart-details/', views.cart_details, name='cart_details'),
    path('checkout/', views.checkout, name='checkout'),

    path('payment/success/<str:str_data>/', views_payment.payment_complete, name='payment_complete'),
    path('payment/cancel/<str:str_data>/', views_payment.payment_cancel, name='payment_cancel'),
    path('payment/fail/<str:str_data>/', views_payment.payment_failed, name='payment_failed'),
    path('payment/check/<str:str_data>/', views_payment.payment_check, name="payment_check"),
]

