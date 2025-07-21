from django.shortcuts import render,redirect, get_object_or_404
from .user_permission import checkUserPermission
from .models import MenuList, ProductMainCategory, ProductSubCategory , Author, Product
from frontend.models import Customer
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth import login, logout, authenticate
# Create your views here.

def paginate_data(request, page_num, data_list):
    items_per_page, max_pages = 10, 10
    paginator = Paginator(data_list, items_per_page)
    last_page_number = paginator.num_pages

    try:
        data_list = paginator.page(page_num)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)

    current_page = data_list.number
    start_page = max(current_page - int(max_pages / 2), 1)
    end_page = start_page + max_pages

    if end_page > last_page_number:
        end_page = last_page_number + 1
        start_page = max(end_page - max_pages, 1)

    paginator_list = range(start_page, end_page)
    return data_list, paginator_list, last_page_number


@login_required
def dashboard_view(request):

    return render(request,'home/home.html')


def login_view(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']

        
        profile = Customer.objects.get(phone=phone)
        user = authenticate(request, username=profile.user.username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully!")

        next_url = request.GET.get('next')
        if next_url:
            next_url = next_url.strip()
        else:
            next_url = "dashboard"
        return redirect(next_url)
            
    return render(request, 'user_login.html')


@login_required
def dashboard_settings(request):
    get_setting_menu = MenuList.objects.filter(module_name= "Setting", is_active=True)
    
    context = {
        "get_setting_menu": get_setting_menu,
    }
    return render(request, 'home/setting_dashboard.html', context)


@login_required
def product_main_category_list_view(request):

    if not checkUserPermission(request, "can_view", "/backend/product-main-category-list/"):
        return render (request, '403.html')
    
    product_main_categories= ProductMainCategory.objects.filter(is_active=True).order_by('-id')
    #paginator = Paginator(product_main_categories, 1)
    page_number = request.GET.get('page', 1)
    product_main_categories, paginator_list, last_page_number = paginate_data(request, page_number, product_main_categories)
    context = {
        'paginator_list': paginator_list,
        'last_page_number': last_page_number,
        'product_main_categories': product_main_categories,
    }
    return render (request, 'product/main_category_list.html', context)


# Main category 
@login_required
def add_product_main_category(request):
    if not checkUserPermission(request, 'can_edit', '/backend/add-product-main-category'):
        return render(request, '403.html')
    
    if request.method =='POST':
        main_cat_name =request.POST.get('main_cat_name')
        cat_image = request.FILES.get('cat_image')
        description = request.POST.get('description')
        
        product_main_category= ProductMainCategory(
            main_cat_name=main_cat_name,
            cat_image=cat_image,
            description=description,
            created_by =request.user
        )
        product_main_category.save()
        messages.success(request, 'Product Main Category added successfully.')
        return redirect('product_main_category_list')
    return render(request, 'product/add_product_main_category.html')


@login_required
def product_main_category_details(request, cat_slug):
    if not checkUserPermission(request, 'can_view', '/backend/product-main-category-list/'):
        return render(request, '403.html')
    data = get_object_or_404(ProductMainCategory, cat_slug=cat_slug)
    context={
        'data':data
    }
    return render(request, 'product/product_main_category_details.html', context)


@login_required
def product_main_category_update(request, cat_slug):

    if not checkUserPermission(request, 'can_update','/backend/product-main-category-list/'):
        return render(request, '403.html')
    
    data = get_object_or_404(ProductMainCategory, cat_slug=cat_slug)

    if request.method == 'POST':
        main_cat_name =request.POST.get('main_cat_name')
        cat_image = request.FILES.get('cat_image')
        description = request.POST.get('description')
        data.main_cat_name = main_cat_name

        if 'cat_image' in request.FILES:
            data.cat_image = cat_image
            
        data.description = description
        data.updated_by = request.user
        data.save()
        return redirect('product_main_category_list')
    return render(request, 'product/add_product_main_category.html',{'data':data} )

@login_required
def product_main_category_delete(request, id):
    if not checkUserPermission(request, 'can_delete','/backend/product-main-category-list/'):
        return render(request, '403.html')
    
    sub_category = get_object_or_404(ProductMainCategory, id=id)
    sub_category.delete()
    return redirect('product_main_category_list')

# Sub Category 
@login_required
@login_required(login_url='/custom-login/')
def product_sub_category_list_view(request):

    if not checkUserPermission(request, "can_view", "/backend/product-sub-category-list/"):
        return render (request, '403.html')
    
    product_main_categories= ProductSubCategory.objects.filter(is_active=True).order_by('-id')

    paginator = Paginator(product_main_categories, 1)
    page_number = request.GET.get('page', 1)
    product_main_categories, paginator_list, last_page_number = paginate_data(request, page_number, product_main_categories)

    context = {
        'paginator_list': paginator_list,
        'last_page_number': last_page_number,
        'product_sub_categories': product_main_categories,
    }
    
    return render (request, 'product/sub_category_list.html', context)

def add_product_sub_category(request):

    if not checkUserPermission(request, 'can_edit', '/backend/product-sub-category-list/'):
        return render(request, '403.html')
    
    if request.method =='POST':
        sub_cat_name=request.POST.get('sub_cat_name')
        main_category_id =request.POST.get('main_category')
        sub_cat_image = request.FILES.get('sub_cat_image')

        main_category=ProductMainCategory.objects.filter(id=main_category_id, is_active=True).first()

        product_main_category= ProductSubCategory(
            sub_cat_name=sub_cat_name,
            main_category=main_category,
            sub_cat_image=sub_cat_image,
            created_by =request.user
        )
        product_main_category.save()
        messages.success(request, 'Product Main Category added successfully.')
        return redirect('product_sub_category_list')
    
    return render(request, 'product/add_product_sub_category.html',{
        'main_categories': ProductMainCategory.objects.filter(is_active=True),
        'selected_main_category': None
    })

def product_sub_category_update(request,sub_cat_slug):

    if not checkUserPermission(request, 'can_update','/backend/product-Sub-category-list/'):
        return render(request, '403.html')
    
    data = get_object_or_404(ProductSubCategory, sub_cat_slug=sub_cat_slug)
    main_categories = ProductMainCategory.objects.filter(is_active=True)
    

    if request.method == 'POST':
        sub_cat_name=request.POST.get('sub_cat_name')
        main_category_id =request.POST.get('main_category')
        sub_cat_image = request.FILES.get('sub_cat_image')

        main_category=ProductMainCategory.objects.filter(id=main_category_id, is_active=True).first()

        data.sub_cat_name = sub_cat_name
        data.main_category = main_category

        if 'sub_cat_image' in request.FILES:
            data.sub_cat_image = sub_cat_image

        data.updated_by = request.user
        data.save()

        return redirect('product_sub_category_list')
    context = {
        'data':data,
        'main_categories': main_categories,
        'selected_main_category': data.main_category,
        
    }
    return render(request, 'product/add_product_sub_category.html',context )


def product_sub_category_details(request, sub_cat_slug):
    if not checkUserPermission(request, 'can_view', '/backend/product-sub-category-list/'):
        return render(request, '403.html')
    
    data = get_object_or_404(ProductSubCategory, sub_cat_slug=sub_cat_slug)
    context={
        'data':data
    }
    return render(request, 'product/product_sub_category_details.html', context)


def product_sub_category_delete(request, id):
    if not checkUserPermission(request, 'can_delete','/backend/product-main-category-list/'):
        return render(request, '403.html')
    
    sub_category = get_object_or_404(ProductSubCategory, id=id)
    sub_category.delete()
    return redirect('product_sub_category_list')


# Author 
def author_list(request):
    if not checkUserPermission(request, 'can_view', '/backend/author_list/'):
        return render(request, '403.html')
    
    author_list= Author.objects.filter(is_active=True).order_by('-id')
    paginator = Paginator(author_list, 1)
    page_number = request.GET.get('page', 1)
    author_list, paginator_list, last_page_number = paginate_data(request, page_number, author_list)
    context = {
        'paginator_list': paginator_list,
        'last_page_number': last_page_number,
        'author_list': author_list,
    }
    return render (request, 'author/author_list.html', context)
    

def author_details(request, author_slug):
    if not checkUserPermission(request, 'can_view', '/backend/author-list/'):
        return render(request, '403.html')
    
    authors = get_object_or_404(Author, author_slug=author_slug)
    context={
        'authors':authors
    }
    return render(request, 'author/author_details.html', context)


def author_delete(request, id):
    if not checkUserPermission(request, 'can_delete','/backend/author-list/'):
        return render(request, '403.html')
    
    sub_category = get_object_or_404(Author, id=id)
    sub_category.delete()
    return redirect('author_list')

def add_author(request):

    if not checkUserPermission(request, 'can_edit', '/backend/author-list/'):
        return render(request, '403.html')
    
    if request.method =='POST':
        author_name=request.POST.get('author_name')
        description =request.POST.get('description')
        dob =request.POST.get('dob')
        author_image = request.FILES.get('author_image')

        product_main_category= Author(
            author_name=author_name,
            description=description,
            dob=dob,
            author_image=author_image,
            created_by =request.user,
            created_at = now()
        )
        product_main_category.save()
        messages.success(request, 'Product Main Category added successfully.')
        return redirect('author_list')
    
    return render(request, 'author/add_author.html')


def author_update(request, author_slug):

    if not checkUserPermission(request, 'can_update','/backend/author-list/'):
        return render(request, '403.html')
    
    data = get_object_or_404(Author, author_slug=author_slug)

    if request.method == 'POST':
        author_name =request.POST.get('author_name')
        author_image = request.FILES.get('author_image')
        dob = request.POST.get('dob')
        description = request.POST.get('description')

        data.author_name = author_name

        if 'author_image' in request.FILES :
           data.author_image = author_image

        data.description = description
        data.dob = dob
        data.updated_by = request.user
        data.save()
        return redirect('author_list')
    return render(request, 'author/add_author.html',{'data':data} )


# product 

def product_list(request):
    if not checkUserPermission(request, "can_view", "/backend/product-list/"):
        return render(request,"403.html")

    products = Product.objects.filter(is_active=True).order_by('-id')
    page_number = request.GET.get('page', 1)
    products, paginator_list, last_page_number = paginate_data(request, page_number, products)

    context = {
        'paginator_list': paginator_list,
        'last_page_number': last_page_number,
        'products': products,
    }

    return render(request, "product/product_list.html", context)


def add_new_product(request):
    if not checkUserPermission(request, "can_add", "/backend/product-list/"):
        return render(request,"403.html")

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        discount_price = request.POST.get('discount_price')
        discount_percentage = request.POST.get('discount_percentage')
        description = request.POST.get('description')
        main_category_id = request.POST.get('main_category')
        sub_category_id = request.POST.get('sub_category')
        author_id = request.POST.get('author')
        image = request.FILES.get('product_image')

        if not main_category_id or not sub_category_id or not product_name or not price or not stock:
            messages.error(request, 'All fields are required.')
            return redirect('add_new_product')
        main_category=ProductMainCategory.objects.filter(id=main_category_id, is_active=True).first()

        if not main_category:
            messages.error(request, 'Invalid main category selected.')
            return redirect('add_new_product')
        
        sub_category=ProductSubCategory.objects.filter(id=sub_category_id, is_active=True).first()

        if not sub_category:
            messages.error(request, 'Invalid Sub category selected.')
            return redirect('add_new_product')
        
        author_instance = Author.objects.filter(id=author_id, is_active=True).first()

        if not author_instance:
            messages.error(request, 'Invalid Author selected.')
            return redirect('add_new_product')
        
        product = Product(
            product_name=product_name,
            product_image=image,
            price=price,
            author=author_instance,
            stock=stock,
            discount_price=discount_price,
            discount_percentage=discount_percentage,
            description=description,
            main_category=main_category,
            sub_category=sub_category,
            created_by=request.user
        )
        product.save()
        
        messages.success(request, 'Product added successfully.')
        return redirect('product_list')

    main_categories= ProductMainCategory.objects.filter(is_active=True)
    sub_categories = ProductSubCategory.objects.filter(is_active=True)
    authors = Author.objects.filter(is_active=True)

    context = {
        'main_categories': main_categories,
        'sub_categories': sub_categories,
        'authors': authors
    }
    return render(request, 'product/add_new_product.html',context)


def product_edit(request, id):
    if not checkUserPermission(request, "can_update", "/backend/product-list/"):
        return render(request,"403.html")

    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product.product_name = request.POST.get('product_name')

        product_image = request.FILES.get('product_image')

        if product_image:
            product.product_image = product_image

        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.description = request.POST.get('description')
        product.discount_percentage = request.POST.get('discount_percentage')
        product.discount_price = request.POST.get('discount_price')
        product.main_category = get_object_or_404(ProductMainCategory, id=request.POST.get('main_category'))
        product.sub_category = get_object_or_404(ProductSubCategory, id=request.POST.get('sub_category'))
        product.updated_by = request.user
        product.save()
        
        messages.success(request, 'Product updated successfully.')
        return redirect('product_list')
    main_categories = ProductMainCategory.objects.filter(is_active=True)
    sub_categories = ProductSubCategory.objects.filter(is_active=True)
    authors = Author.objects.filter(is_active=True)
    context = {
        'product': product,
        'main_categories': main_categories,
        'sub_categories': sub_categories,
        'authors':authors
    }
    return render(request, 'product/product_edit.html', context)



def product_detail(request, product_slug):
    if not checkUserPermission(request, "can_view", "/backend/product-list/"):
        return render(request,"403.html")

    product = get_object_or_404(Product, product_slug=product_slug)
    
    context = {
        'product': product,
    }
    return render(request, 'product/product_detail.html', context)


def delete_product(request, id):

    if not checkUserPermission(request, 'can_delete', '/backend/product-list/'):
        return render(request, '403.html')
    
    product = get_object_or_404(Product, id=id)
    product.is_active =False
    product.save()

    messages.success(request, 'Product deleted successfully.')
    return redirect('product_list')

