from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import is_safe_url

from product.models import Category

# Create your views here.
from user.models import UserProfile


def index(request):
    return HttpResponse('sss')


def login_form(request):
    last_url = request.META.get('HTTP_REFERER')  # get last url

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect  to a success page
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            if userprofile.image:
                request.session['userimage'] = userprofile.image.url

            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "خطا در ورود !! نام کاربری یا کلمه عبور اشتباه است.")
            return HttpResponseRedirect(last_url)


def signup(request):
    category = Category.objects.all()
    context = {'category': category, }
    return render(request, "signup.html", context)


def login_page(request):
    category = Category.objects.all()
    context = {'category': category, }
    return render(request, "login.html", context)


def logout_func(request):
    logout(request)
    return HttpResponseRedirect("/")
