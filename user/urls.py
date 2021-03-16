from django.contrib.auth import views
from django.urls import path

from . import views as user_view

app_name = "user"
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

urlpatterns += [
    path('', user_view.Index.as_view(), name='profile'),
    path('hlogin', user_view.login_form_header, name='login_header'),
    path('profile_edit', user_view.ProfileEdit.as_view(), name='profileEdit'),
    path('address', user_view.edit_address, name='editAddress'),
    path('changepassword', user_view.change_password, name='changePassword'),
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
