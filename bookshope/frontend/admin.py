from django.contrib import admin
from .models import OrderCart, Order
# Register your models here.

admin.site.register(Order)
admin.site.register(OrderCart)
