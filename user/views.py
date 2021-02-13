from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import is_safe_url

from product.models import Category

# Create your views here.
from user.forms import SignUpForm, EditUserInfoForm, EditProfileInfoForm
from user.models import UserProfile


# @login_required(login_url='/login')  # check login
def index(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category, 'profile': profile}
    return render(request, "user_profile.html", context)


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
            return HttpResponseRedirect('/login')


def login_page(request):
    category = Category.objects.all()
    context = {'category': category, }
    return render(request, "login.html", context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "حساب کاربری شما ایجاد شد.")

            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form}
    return render(request, "signup.html", context)


def logout_func(request):
    logout(request)
    return HttpResponseRedirect("/")


def edit_info_page(request):
    if request.method == 'POST':
        form_user = EditUserInfoForm(request.POST)
        form_profile = EditProfileInfoForm(request.POST)
        if form_user.is_valid() and form_profile.is_valid():
            user_data = User.objects.get(id=request.user.id)

            # user_data.first_name = form_user.cleaned_data.get('firstname')
            # user_data.last_name = form_user.cleaned_data.get('lastname')
            user_data.save()

            profile_data = UserProfile()
            profile_data.phone = form_profile.cleaned_data.get('phone')
            profile_data.state = form_profile.cleaned_data.get('state')
            profile_data.city = form_profile.cleaned_data.get('city')
            profile_data.address = form_profile.cleaned_data.get('address')
            profile_data.postal_code = form_profile.cleaned_data.get('zipcode')
            profile_data.save()
            messages.success(request, "اطلاعات شما ثبت شد.")
            return HttpResponseRedirect('/user/edit')
        else:
            messages.error(request, "خطا در ثبت اطلاعات.")
            return HttpResponseRedirect('/user/edit')

    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category, 'profile': profile}
    return render(request, "edit_information.html", context)
