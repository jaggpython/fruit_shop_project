from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search/', views.product_list, name='product_search'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),

    path('settings/', views.settings_view, name='settings'),
    path('settings/update/<int:id>/', views.update_product, name='update_product'),
    path('settings/delete/<int:id>/', views.delete_product, name='delete_product'),

    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('cart/increase/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/', views.cart, name='cart'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
