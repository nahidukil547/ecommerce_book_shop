from django.urls import path
from . import views
urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('setting-dashboard/', views.dashboard_settings, name='setting-dashboard'),

    path('product-main-category-list/', views.product_main_category_list_view, name='product_main_category_list'),
    path('product-sub-category-list/', views.product_sub_category_list_view, name='product_sub_category_list'),
    path('author-list/', views.author_list, name='author_list'),
    path('product-list/', views.product_list, name='product_list'),


    path('add-product-main-category/', views.add_product_main_category, name='add_product_main_category'),
    path('add-product-sub-category/', views.add_product_sub_category, name='add_product_sub_category'),
    path('add-author/', views.add_author, name='add_author'),
    path('add-new-product/', views.add_new_product, name='add_new_product'),

    path('product-main-category-details/<str:cat_slug>', views.product_main_category_details, name='product_main_category_details'),
    path('product-sub-category-details/<str:sub_cat_slug>', views.product_sub_category_details, name='product_sub_category_details'),
    path('author-details/<slug:author_slug>/', views.author_details, name='author_details'),
    path('product=detail/<slug:product_slug>/', views.product_detail, name='product_detail'),

    
    path('product-main-category-update/<str:cat_slug>', views.product_main_category_update, name='product_main_category_update'),
    path('product-sub-category-update/<str:sub_cat_slug>', views.product_sub_category_update, name='product_sub_category_update'),
    path('author-update/<str:author_slug>', views.author_update, name='author_update'),
    path('product-edit/<int:id>', views.product_edit, name='product_edit'),

    path('product-sub-category-delete/<int:id>', views.product_sub_category_delete, name='product_sub_category_delete'),
    path('product-main-category-delete/<int:id>', views.product_main_category_delete, name='product_main_category_delete'),
    path('author-delete/<int:id>', views.author_delete, name='author_delete'),
    path('delete-product/<int:id>', views.delete_product, name='delete_product'),
]
