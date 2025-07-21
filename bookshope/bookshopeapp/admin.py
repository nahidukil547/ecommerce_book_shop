from django.contrib import admin
from .models import ( ProductMainCategory,ProductSubCategory, UserPermission, Product )
from frontend.models import Customer

# Register your models here.


@admin.register(ProductMainCategory)
class ProductMainCategoryAdmin(admin.ModelAdmin):
    list_display         = ('main_cat_name', 'cat_slug', 'cat_ordering', 'created_by', 'updated_by', 'created_at', 'updated_at', 'is_active')
    list_filter          = ('is_active',)
    search_fields        = ('main_cat_name', 'cat_slug')
    ordering             = ('cat_ordering',) 



@admin.register(ProductSubCategory)
class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_display         = ('sub_cat_name', 'main_category', 'sub_cat_ordering', 'created_by', 'updated_by', 'created_at', 'updated_at', 'is_active')
    list_filter          = ('is_active',)
    search_fields        = ('sub_cat_name', 'sub_cat_slug')
    ordering             = ('sub_cat_ordering',) 


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = (
        'get_customer_name', 
        'get_menu_name', 
        'can_view', 
        'can_add', 
        'can_update', 
        'can_delete', 
        'created_at', 
        'updated_at', 
        'is_active'
    )
    list_filter = ('is_active', 'can_view', 'can_add', 'can_update', 'can_delete')
    search_fields = ('user__customer__name', 'menu__menu_name')
    ordering = ('-created_at',)

    def get_customer_name(self, obj):
        customer = getattr(obj.user, 'customer', None)
        return customer.name if customer else obj.user.username
    get_customer_name.short_description = 'Customer Name'

    def get_menu_name(self, obj):
        return obj.menu.menu_name
    get_menu_name.short_description = 'Menu Name'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display         = ('product_name', 'main_category', 'sub_category','price','stock', 'created_by', 'updated_by', 'is_active')
    list_filter          = ('is_active','main_category', 'sub_category')
    search_fields        = ('product_name', 'main_category__main_cat_name', 'sub_category__sub_cat_name', 'product_slug')
    ordering             = ('product_name',) 