from django.urls import path

from . import views

app_name = 'payment'
urlpatterns = [
    path('request/<int:id>/', views.send_request, name='request'),
    path('verify/', views.verify, name='verify'),
]
