from django.urls import path, re_path

from . import views

app_name = 'product'
urlpatterns = [
    re_path(r'(?P<id>\d+)/(?P<slug>[-\w]+)/', views.index, name="product_details"),
    path('addcomment/<int:id>/', views.add_comment, name="add_comment"),
    path('ajaxcolor/', views.ajaxcolor, name="ajaxcolor"),

]
