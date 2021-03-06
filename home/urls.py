from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index),
    path('contact/', views.contact, name='contact'),
    path('aboutus/', views.aboutus, name='aboutus'),
]
