from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home.html'),
    path('about', views.about, name="about.html"),
    path('products', views.products, name="products.html"),
    path('location', views.contact, name="location.html"),  
    path('checkout', views.checkout, name="checkout.html"),
    path('mycart', views.mycart, name="mycart.html"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order")
]

from django.contrib import admin
#admin header custom
admin.site.site_title = 'Lensmart Admin'
admin.site.site_header = 'Lensmart administration'
# admin.site.index_title = 'Lensmart admin'