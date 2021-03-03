from django.urls import path

from . import views

app_name = "user"
urlpatterns = [
    path('', views.index, name='add_comment'),
    path('login', views.login_form, name='login'),
    path('edit', views.edit_info_page, name='editProfileInformation'),
    path('address', views.edit_address, name='editAddress'),
    path('changepassword', views.change_password, name='changepassword'),
    path('orders', views.user_orders, name='userOrders'),
    path('comments', views.user_comments, name='userComments'),
    path('orderdetails/<int:id>', views.order_details, name='ordersDetails'),

]
