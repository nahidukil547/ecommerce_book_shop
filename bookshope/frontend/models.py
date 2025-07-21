from django.db import models
from bookshopeapp.models import Author,Product ,ProductMainCategory ,ProductSubCategory 
from django.contrib.auth.models import User 
import datetime
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=100,null=True, blank=True)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    address= models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class OrderCart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='order_cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_order= models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_amount(self):
        return_value=float(self.quantity) * float(self.product.price)
        return return_value
    
    class Meta:
        db_table = 'order_cart'

    def __str__(self):
        return f"{self.customer} - {self.product.product_name} ({self.quantity})"
    


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    order_number = models.CharField(max_length=100, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    billing_address = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    shipping_charge = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    discount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    coupon_discount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    vat_amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    tax_amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    paid_amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    due_amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    grand_total = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order_number)+" ("+str(self.customer)+" - "+str(self.created_at)+")"

    class Meta:
        db_table = 'orders'

    def save(self, *args, **kwargs):
        if not self.order_number:
            current_year =datetime.date.today().year
            current_month = datetime.date.today().month
            current_day = datetime.date.today().day
            current_customer_id =self.customer.id

            last_order = Order.objects.filter(order_number__startswith=f"{current_year}{current_month:02d}")
            increase_number= 1
            new_order_number = f"{current_year}{current_month:02d}{last_order.count() + increase_number:04d}{current_day:02d}{current_customer_id}"

            while Order.objects.filter(order_number = new_order_number).exists():
                increase_number += 1
                new_order_number = f"{current_year}{current_month:02d}{last_order.count() + increase_number:04d}{current_day:02d}{current_customer_id}"
            self.order_number = new_order_number
        super().save(*args, **kwargs)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='order_details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    is_discount = models.BooleanField(default=False)
    discount_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return str(self.order.order_number)+" ("+str(self.product)+" - "+str(self.quantity)+")"

    class Meta:
        db_table = 'order_details'


class OnlinePaymentRequest(models.Model):
    order = models.ForeignKey(Order, related_name='order_payment_requests', on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_status_list = [('Pending', 'Pending'), ('Paid', 'Paid'), ('Cancelled', 'Cancelled'), ('Failed', 'Failed')]
    payment_status = models.CharField(max_length=15, choices=payment_status_list, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_request_created_by')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "online_payment_request"

class OrderPayment(models.Model):
    order = models.ForeignKey(Order, related_name='order_payments', on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    transaction_id = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order.order_number)+" ("+str(self.payment_method)+" - "+str(self.amount)+")"

    class Meta:
        db_table = 'order_payments'
