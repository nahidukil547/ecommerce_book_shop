from bookshopeapp.models import Author,Product ,ProductMainCategory ,ProductSubCategory 
from .models import Customer, OrderCart
from .views import cart_amount_summary
from django.urls import reverse

def get_cart_item(request):

    if request.user.is_authenticated:
        try:
            customer= Customer.objects.filter(user=request.user).first()
            cart_items = OrderCart.objects.filter(customer=customer, is_active=True, is_order=False)
        except OrderCart.DoesNotExist:
            cart_items = []
    else:
        cart_items = []

    amount_summary=cart_amount_summary(request)

    return {'cart_item_count': len(cart_items), 'cart_items': cart_items, 'amount_summary': amount_summary}



# def get_absolute_url(self):
#     return reverse('products_detail', kwargs={'slug': self.product_slug})
