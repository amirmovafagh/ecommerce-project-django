from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='add_comment'),
    path('login', views.login_form, name='login'),

]
