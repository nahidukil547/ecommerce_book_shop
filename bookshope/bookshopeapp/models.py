from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import unicodedata
from django.urls import reverse
# Create your models here.
class MenuList(models.Model):
    module_name = models.CharField(max_length=100, db_index=True)
    menu_name = models.CharField(max_length=100,unique=True, db_index=True)
    menu_url = models.URLField(max_length=250, unique=True)
    menu_icon = models.CharField(max_length=100, blank=True, null=True)
    parent_id = models.IntegerField(default=0)
    is_main_menu= models.BooleanField(default=False)
    is_sub_menu = models.BooleanField(default=False)
    is_sub_child_menu = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    delete_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    deleted= models.BooleanField(default=False)
    
    class Meta:
        db_table= 'menu_list'
    
    def __str__(self):
        return self.module_name
    
class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permission')
    menu = models.ForeignKey(MenuList, on_delete=models.CASCADE, related_name="menu_for_permission") 
    can_view      = models.BooleanField(default=False)
    can_add       = models.BooleanField(default=False)
    can_update    = models.BooleanField(default=False)
    can_delete    = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    created_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by_user") 
    updated_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="updated_by_user", blank=True, null=True) 
    is_active     = models.BooleanField(default=True)
    deleted_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="deleted_by_user", blank=True, null=True)
    deleted       = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table= 'user_permission'

    def __str__(self):
        return self.menu.menu_name

    
class ProductMainCategory(models.Model):
    main_cat_name = models.CharField(max_length=100, unique=True)
    cat_slug      = models.SlugField(max_length=150, unique=True, blank=True)
    cat_image     = models.ImageField(upload_to='ecommerce/category_images/', blank=True, null=True)
    cat_icon     = models.CharField(max_length=100, blank=True, null=True)
    description   = models.TextField(blank=True, null=True)
    cat_ordering  = models.IntegerField(default=0,blank=True, null=True)
    created_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_created_by')
    updated_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_updated_by', blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    is_active     = models.BooleanField(default=True)

    class Meta:
        db_table = 'product_main_category'
        verbose_name_plural = 'Product Categories'
        ordering = ['-is_active','cat_ordering']

    def __str__(self):
        return self.main_cat_name
    
    def save (self, *args, **kwargs):
        if not self.cat_slug and self.main_cat_name:
            base_slug = slugify(self.main_cat_name) 
            slug = base_slug
            num=1
            while ProductMainCategory.objects.filter(cat_slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num+=1
            self.cat_slug = slug
        super().save(*args, **kwargs)

class ProductSubCategory(models.Model):
    main_category= models.ForeignKey(ProductMainCategory, on_delete=models.CASCADE, related_name='sub_categories')
    sub_cat_name= models.CharField(max_length=100, unique=True)
    sub_cat_slug      = models.SlugField(max_length=150, unique=True, blank=True)
    sub_cat_image     = models.ImageField(upload_to='ecommerce/sub_category_images/', blank=True, null=True)
    sub_cat_icon     = models.CharField(max_length=100, blank=True, null=True)
    sub_cat_ordering  = models.IntegerField(default=0)
    created_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sub_category_created_by')
    updated_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sub_category_updated_by', blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    is_active     = models.BooleanField(default=True)

    def __str__(self):
        return self.sub_cat_name
    
    class Meta:
        db_table = 'product_sub_category'
        verbose_name_plural = 'Product Categories'
        ordering = ['-is_active','sub_cat_ordering']

    def save(self, *args, **kwargs):
        if not self.sub_cat_slug and self.sub_cat_name:
            base_slug= slugify(self.sub_cat_name)
            slug = base_slug
            num = 1
            while ProductSubCategory.objects.filter(sub_cat_name=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num+=1
            self.sub_cat_slug = slug
        super().save(*args, **kwargs)

            


class Author(models.Model):
    author_name = models.CharField(max_length=100, unique=True)
    author_slug = models.SlugField(max_length=150, unique=True, blank=True)
    author_image = models.ImageField(upload_to='ecommerce/author_image/', blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors_updated_by', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=False, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'author'
        verbose_name_plural = 'author'
        ordering = ['-is_active']

    def __str__(self):
        return self.author_name
    
    def save(self, *args, **kwargs):
        if not self.author_slug and self.author_name:

            base_slug =slugify(self.author_name)
            slug = base_slug
            num = 1
            while Author.objects.filter(author_slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.author_slug = slug
        super().save(*args, **kwargs)



class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_slug = models.SlugField(max_length=150, unique=True, blank=True)
    product_image = models.ImageField(upload_to='ecommerce/product_images/', blank=True, null=True)
    main_category = models.ForeignKey(ProductMainCategory, on_delete=models.CASCADE, related_name='products')
    sub_category = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True,related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    total_views = models.PositiveIntegerField(default=0)
    discount_percentage = models.PositiveIntegerField(default=0, blank=True, null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_updated_by', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    is_active = models.BooleanField(default=True)





    class Meta:
        db_table = 'products'
        verbose_name_plural = 'Products'
        ordering = ['-is_active']

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        if not self.product_slug and self.product_name:
            base_slug = slugify(self.product_name)
            slug = base_slug
            num = 1
            while Product.objects.filter(product_slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.product_slug = slug
        super().save(*args, **kwargs)
