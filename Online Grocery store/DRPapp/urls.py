
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('checkout', views.checkout, name='checkout'),
    path('show_cart', views.show_cart, name='show_cart'),
    path('feedback', views.feedback, name='feedback'),
    path('home', views.home, name='home'),
    path('shop/<str:category_name>', views.shop, name='shop'),
    path('cart/<int:id>', views.cart, name='cart'),
    path('update_cart_quantity',views.update_cart_quantity,name='update_cart_quantity'),
    path('logout', views.logout,name='logout'),
    path('email',views.email,name='email'),
    path('add_category', product_category_view, name = 'image_upload'),
    path('success', success, name = 'success'),
    path('add_product', Product_details_view, name = 'add_product'),
    path('thankyou', thankyou, name = 'thankyou'),

]

