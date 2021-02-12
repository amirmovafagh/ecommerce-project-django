from django.urls import path

from . import views

urlpatterns = [
    path('', views.order, name='order'),
    path('addproduct/<int:id>', views.add_product, name='addproduct'),
    path('removefromcart/<int:id>', views.remove_from_cart, name='removeFromCart'),
    path('shopcart', views.shopcart, name='addproduct'),
    path('orderproduct', views.order_products, name='orderProducts'),
    path('checkPrice', views.order_checkPrice, name='orderCheckPrice'),
]
