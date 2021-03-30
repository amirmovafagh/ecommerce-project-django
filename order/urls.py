from django.urls import path

from . import views

app_name = 'order'
urlpatterns = [
    path('', views.order, name='order'),
    path('addproduct/<int:id>', views.add_product, name='addproduct'),
    path('removefromcart/<int:id>', views.remove_from_cart, name='removeFromCart'),
    path('shopcart', views.shopcart, name='shopcart'),
    path('orderproduct', views.order_products_address, name='orderProducts'),
    path('paymentmethods', views.payment_methods, name='paymentmethods'),
    path('checkPrice', views.order_check_price, name='orderCheckPrice'),
]
