from django.contrib.auth import views
from django.urls import path

from . import views as user_view

app_name = "user"
urlpatterns = [
    path('', user_view.Index.as_view(), name='profile'),
    path('hlogin', user_view.login_form_header, name='login_header'),
    path('profile_edit', user_view.ProfileEdit.as_view(), name='profileEdit'),
    path('address', user_view.AddressList.as_view(), name='address'),
    path('address/edit/<int:id>/', user_view.AddressUpdate.as_view(), name='addressEdit'),
    path('address/remove/<int:id>/', user_view.address_delete, name='addressDelete'),
    path('orders', user_view.user_orders, name='userOrders'),
    path('comments', user_view.user_comments, name='userComments'),
    path('orderdetails/<int:id>', user_view.order_details, name='ordersDetails'),

    path('admin/', user_view.admin_user, name='admin'),
    path('admin/products/', user_view.AdminProductList.as_view(), name='adminProducts'),
    path('admin/products/create/', user_view.AdminProductCreate.as_view(), name='adminProductsCreate'),
    path('admin/products/update/<int:pk>', user_view.AdminProductUpdate.as_view(), name='adminProductsUpdate'),
    path('admin/products/delete/<int:pk>', user_view.AdminProductDelete.as_view(), name='adminProductsDelete'),
    path('admin/orders/', user_view.admin_orders, name='adminOrders'),
]
