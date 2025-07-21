from django.shortcuts import render, redirect, get_object_or_404
from bookshopeapp.models import Author,Product ,ProductMainCategory ,ProductSubCategory 
from .models import Customer, OrderCart, OrderDetail, Order
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from decimal import Decimal
from .views_payment import create_payment_request
# Create your views here.

def home (request):
    authors = Author.objects.annotate(product_count=Count('products'))[:8]
    product = Product.objects.filter(is_featured=True, is_active=True).order_by('-id')[:8]
    best_selling = Product.objects.filter(is_featured=True, is_active=True).order_by('id')[:5]
    main_category = ProductMainCategory.objects.filter(is_active = True)[:10]
    sub_category = ProductSubCategory.objects.filter(is_active = True)
    

    context = {
        'authors': authors,
        'products': product,
        'main_category': main_category,
        'sub_categories': sub_category,
        'best_selling': best_selling
    }
    return render(request, 'frontend/home.html', context)

def login(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']

        
        profile = Customer.objects.get(phone=phone)
        user = authenticate(request, username=profile.user.username, password=password)
        if user:
            auth_login(request, user)
            messages.success(request, "Logged in successfully!")

        next_url = request.GET.get('next')
        if next_url:
            next_url = next_url.strip()
        else:
            next_url = "home"
        return redirect(next_url)
    return render(request, 'frontend/login_register.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home')


def register(request):
    if request.method =='POST':
        username = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        dob = request.POST['dob']
        password = request.POST['password']
        address = request.POST['address']

        if Customer.objects.filter(phone=phone).exists():
            return render(request, 'website/user/register.html', {'error': 'Phone already taken'})
        
        user = User.objects.create_user(username=phone,  email=email, password=password)
        Customer.objects.create(user=user, name=username, phone=phone, date_of_birth=dob, address=address)

        messages.success(request, "Logged in successfully!")

        next_url = request.GET.get('next')
        if next_url:
            next_url = next_url.strip()
        else:
            next_url = "home"
        
        return redirect(next_url)

    return render(request, 'frontend/login_register.html')

def cart_amount_summary(request):
    sub_total_amount = 0
    total_vat = 0
    total_discount = 0
    grand_total = 0

    if request.user.is_authenticated:
        customer= Customer.objects.filter(user=request.user).first()
        cart_items = OrderCart.objects.filter(customer=customer, is_active=True, is_order=False)

        for item in cart_items:
            sub_total_amount += item.total_amount
            # total_vat += (item.product.price * 0.15)
            # total_discount+= item.product.discount_percentage
    grand_total = (sub_total_amount + total_vat) - total_discount 

    return {'sub_total_amount': sub_total_amount, 'total_vat': total_vat, 'total_discount': total_discount, 'grand_total': grand_total}
    


def product_details(request,product_slug):
    product= get_object_or_404(Product, product_slug=product_slug)
    main_category = ProductMainCategory.objects.filter(is_active = True)[:10]
    sub_category = ProductSubCategory.objects.filter(is_active = True)

    context={
        'product':product,
        'main_category': main_category,
        'sub_categories': sub_category,
    }

    if not product:
        messages.error(request, "Product not found.")
        return redirect('home')
    
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        product_cart= OrderCart.objects.filter(customer=customer, product=product, is_active=True, is_order=False).first()
        
        if product_cart:
            product.product_cart = product_cart
    
    return render(request, 'frontend/product_details.html', context )


def add_or_update_cart(request):
    is_authenticated = request.user.is_authenticated

    if is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 0))
        

        try:
            
            isRemoved = False

            cart_item, created = OrderCart.objects.update_or_create(
                customer=customer, product_id=product_id, is_order=False, is_active=True,
                defaults={'quantity': quantity}
            )
            if not created:
                if quantity<=0:
                    cart_item.is_active = False
                    isRemoved =True
                cart_item.quantity= quantity
                cart_item.save()
            amount_summary = cart_amount_summary(request)
            cart_item_count = OrderCart.objects.filter(customer=customer, is_active = True, is_order=False).count()

            response = {
                    'status': 'success',
                    'message': 'Cart updated successfully',
                    'is_authenticated': is_authenticated,
                    'isRemoved': isRemoved,
                    'item_price': cart_item.total_amount,
                    'cart_item_count': cart_item_count,
                    'amount_summary': amount_summary,
                }
            return JsonResponse(response)
        except OrderCart.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Cart item not found', 'is_authenticated': is_authenticated,})
    return JsonResponse({'status': 'error', 'message': 'Invalid request', 'is_authenticated': is_authenticated,}, status=400)


@login_required
def cart_details(request): 
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        customer = None
    # Categories
    main_category = ProductMainCategory.objects.filter(is_active=True)[:10]
    sub_category = ProductSubCategory.objects.filter(is_active=True)

    context = {
        'customer': customer,
        'main_category': main_category,
        'sub_categories': sub_category,
    }

    return render(request, 'frontend/cart_details.html', context)


# @login_required
# def checkout(request):

#     amount_summary = cart_amount_summary(request)
#     grand_total = amount_summary.get('grand_total', 0)

#     if grand_total < 1:
#         messages.error(request, "Your cart is empty. Please add items to your cart before proceeding to checkout.")
#         return redirect('cart')
    
#     if request.method == 'POST':

#         with transaction.atomic():

#             billing_address = request.POST.get('billing_address')
#             customer= Customer.objects.filter(user=request.user).first()

#             if not billing_address:
#                 messages.error(request, "Billing address is required.")
#                 return redirect('checkout')
            
#             cart_items = OrderCart.objects.filter(customer=customer, is_active=True, is_order=False)

#             if len(cart_items) < 1:
#                 messages.error(request, "Your cart is empty. Please add items to your cart before proceeding to checkout.")
#                 return redirect('cart_details')
#             else:

#                 order_obj= Order.objects.create(
#                     customer=customer,
#                     billing_address=billing_address,
                    
#                 )

#                 order_amount, shipping_charge, discount, coupon_discount, vat_amount, tax_amount = 0, 0, 0, 0, 0, 0

#                 for cart_item in cart_items:
#                     order_amount += cart_item.total_amount

#                     OrderDetail.objects.create(
#                         order=order_obj,
#                         product=cart_item.product,
#                         quantity=cart_item.quantity,
#                         unit_price=cart_item.product.price,
#                         total_price=cart_item.total_amount
#                     )

#                 grand_total = (order_amount + shipping_charge + vat_amount + tax_amount) - (discount + coupon_discount)

#                 order_obj.order_amount = order_amount
#                 order_obj.shipping_charge = shipping_charge
#                 order_obj.discount = discount
#                 order_obj.coupon_discount = coupon_discount
#                 order_obj.vat_amount = vat_amount
#                 order_obj.tax_amount = tax_amount
#                 order_obj.due_amount = grand_total
#                 order_obj.grand_total = grand_total
#                 order_obj.save()

#                 messages.success(request, "Order placed successfully.")
#                 return redirect('home')
                #print(f"Order Amount: {order_amount}, Shipping Charge: {shipping_charge}, Discount: {discount}, Coupon Discount: {coupon_discount}, VAT Amount: {vat_amount}, Tax Amount: {tax_amount}, Grand Total: {grand_total}")

                # response_data, response_status = create_payment_request(request, order_obj.id)
                # print(response_data)
                # print(response_status)

                

                # if response_data['status'] == "SUCCESS":
                #     for cart_item in cart_items:
                #         cart_item.is_order = True
                #         cart_item.save()

                #     return redirect(response_data['GatewayPageURL'])
                # elif "error_message" in response_data:
                #     messages.error(request, response_data['error_message'])
                # else:
                #     messages.error(request, 'Failed to payment.')

                

                # return redirect('home')


@login_required
def checkout(request):
    amount_summary = cart_amount_summary(request)
    grand_total = amount_summary.get('grand_total', 0)

    if grand_total < 1:
        messages.error(request, "Your cart is empty. Please add items to your cart before proceeding to checkout.")
        return redirect('cart')

    if request.method == 'POST':
        with transaction.atomic():

            billing_address = request.POST.get('billing_address')
            customer = Customer.objects.filter(user=request.user).first()

            if not billing_address:
                messages.error(request, "Billing address is required.")
                return redirect('checkout')

            cart_items = OrderCart.objects.filter(customer=customer, is_active=True, is_order=False)

            if len(cart_items) < 1:
                messages.error(request, "Your cart is empty. Please add items to your cart before proceeding to checkout.")
                return redirect('cart_details')

            
            order_obj = Order.objects.create(
                customer=customer,
                billing_address=billing_address,
            )

            
            order_amount, shipping_charge, discount, coupon_discount, vat_amount, tax_amount = 0, 0, Decimal('0.0'), 0, 0, 0

            for cart_item in cart_items:
                product = cart_item.product
                quantity = cart_item.quantity
                unit_price = product.price
                discount_percent = product.discount_percentage or 0
                
            
                discounted_price = unit_price * (Decimal('1.0') - discount_percent / Decimal('100'))
                total_price = discounted_price * quantity
                item_discount_amount = (unit_price * quantity) - total_price

                order_amount += total_price
                discount += item_discount_amount
                
                is_discount = False
                if discount > 0:
                    is_discount= True

                OrderDetail.objects.create(
                    order=order_obj,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price,
                    is_discount= is_discount,
                    discount_price= discount
                )

            grand_total = (order_amount + shipping_charge + vat_amount + tax_amount) - (discount + coupon_discount)

            order_obj.order_amount = order_amount
            order_obj.shipping_charge = shipping_charge
            order_obj.discount = discount
            order_obj.coupon_discount = coupon_discount
            order_obj.vat_amount = vat_amount
            order_obj.tax_amount = tax_amount
            order_obj.due_amount = grand_total
            order_obj.grand_total = grand_total

            order_obj.save()



            messages.success(request, "Order placed successfully.")
            
            response_data, response_status = create_payment_request(request, order_obj.id)
            print(response_data)
            print(response_status)

            print("Response Data:", response_data)

            if response_data['status'] == "SUCCESS":
                for cart_item in cart_items:
                    cart_item.is_order = True
                    cart_item.save()

                return redirect(response_data['GatewayPageURL'])
            elif "error_message" in response_data:
                messages.error(request, response_data['error_message'])
            else:
                messages.error(request, 'Failed to payment.')

            return redirect('home')


