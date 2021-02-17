from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import is_safe_url

from product.models import Category

# Create your views here.
from user.forms import SignUpForm, UserUpdateForm, EditProfileInfoForm
from user.models import UserProfile


@login_required(login_url='/login')  # check login
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
            messages.warning(request, "خطا در ورود !! نام کاربری یا رمز عبور اشتباه است.")
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


@login_required(login_url='/login')  # check login
def edit_info_page(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = EditProfileInfoForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "اطلاعات بروز شد.")
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, "خطا در ثبت اطلاعات.")
            return HttpResponseRedirect('/user/edit')

    category = Category.objects.all()
    user_form = UserUpdateForm(instance=request.user)
    profile_form = EditProfileInfoForm(instance=request.user.userprofile)
    context = {'category': category, 'profile_form': profile_form, 'user_form': user_form}
    return render(request, "edit_information.html", context)


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!!
            messages.success(request, "رمز عبور تغییر یافت.")
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'خطا در تغییر رمز عبور.' + str(form.errors))
            return HttpResponseRedirect('/user/changepassword')
    else:

        category = Category.objects.all()
        form = PasswordChangeForm(request.user)

        return render(request, 'change_password.html', {'form': form, 'category': category})
