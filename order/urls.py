from django.urls import path

from . import views

urlpatterns = [
    path('', views.order, name='order'),
    path('addproduct/<int:id>', views.add_product, name='addproduct'),
]
