from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index),
    path('contact/', views.ContactUs.as_view(), name='contact'),
    path('aboutus/', views.aboutus, name='aboutus'),
]
