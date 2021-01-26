from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'(?P<id>[0-9]+)/(?P<slug>[\w-]+)/', views.index, name='product_details'),
    path('addcomment/<int:id>/', views.add_comment, name='add_comment'),

]
