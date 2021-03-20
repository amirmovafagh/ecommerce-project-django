"""ecommerce_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from home import views
from user import views as user_views

urlpatterns = [path('', include('home.urls')),
               path('', include('django.contrib.auth.urls')),
               path('login/', user_views.Login.as_view(), name='login'),
               path('admin/', admin.site.urls),
               path('search/', views.search, name='search'),
               path('search/<int:page>', views.search, name='search'),
               path('faq/', views.faq, name='faq'),
               path('search_auto/', views.search_auto, name='search_auto'),
               path('product/', include('product.urls')),
               path('order/', include('order.urls')),
               path('user/', include('user.urls')),
               path('signup/', user_views.Signup.as_view(), name='signup'),
               re_path(r'^activate/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
                       user_views.activate, name='activate'),
               path('ckeditor/', include('ckeditor_uploader.urls')),
               re_path(r'category/(?P<slug>[-\w]+)/', views.CategoryProductsList.as_view(),
                       name='category_products'),
               re_path(r'category/(?P<slug>[-\w]+)/(?P<page>\d+)/', views.CategoryProductsList.as_view(),
                       name='category_products'),
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # for showing images

# admin.site.site_header = 'Admin'
# admin.site.site_title = 'Administration'
# admin.site.index_title = 'Welcome To Administration'
