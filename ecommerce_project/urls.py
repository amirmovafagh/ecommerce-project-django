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

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('search/', views.search, name='search'),
                  path('faq/', views.faq, name='faq'),
                  path('search_auto/', views.search_auto, name='search_auto'),
                  path('', include('home.urls')),
                  path('product/', include('product.urls')),
                  path('order/', include('order.urls')),
                  path('user/', include('user.urls')),
                  path('signup', user_views.signup, name='signup'),
                  path('login', user_views.login_page, name='login'),
                  path('logout', user_views.logout_func, name='logout'),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('category/<int:id>/<slug:slug>/', views.category_products, name='category_products'),
                  path('category/<int:id>/<slug:slug>/<int:page>', views.category_products, name='category_products'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # for showing images

# admin.site.site_header = 'Admin'
# admin.site.site_title = 'Administration'
# admin.site.index_title = 'Welcome To Administration'
