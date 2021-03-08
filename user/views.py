from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from order.models import Order, OrderProduct
from product.models import Comment

# Create your views here.
from user.forms import SignUpForm, EditProfileInfoForm
from user.models import UserProfile


class Profile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = "edit_information.html"
    fields = ['username', 'email', 'first_name', 'last_name', ]
    success_url = reverse_lazy("user:profile")
    success_message = "اطلاعات بروز شد."

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)


@login_required  # check login
def index(request):
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    last_order = Order.objects.filter(user_id=current_user.id).last()
    context = {'profile': profile, 'lastOrder': last_order}
    return render(request, "user_profile.html", context)


def login_form_header(request):
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
            return HttpResponseRedirect('/user/login')


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
    context = {
        'form': form}
    return render(request, "signup.html", context)


def logout_func(request):
    logout(request)
    return HttpResponseRedirect("/")


# @login_required  # check login
# def edit_info_page(request):
#     if request.method == 'POST':
#         user_form = UserUpdateForm(request.POST, instance=request.user)
#         profile_form = EditProfileInfoForm(request.POST, request.FILES, instance=request.user.userprofile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, "اطلاعات بروز شد.")
#             return HttpResponseRedirect('/user')
#         else:
#             messages.error(request, "خطا در ثبت اطلاعات.")
#             return HttpResponseRedirect('/user/edit')
#
#     user_form = UserUpdateForm(instance=request.user)
#     profile_form = EditProfileInfoForm(instance=request.user.userprofile)
#     context = {'profile_form': profile_form, 'user_form': user_form}
#     return render(request, "edit_information.html", context)


@login_required
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

        form = PasswordChangeForm(request.user)

        return render(request, 'change_password.html', {'form': form, })


@login_required
def edit_address(request):
    return None


@login_required
def user_orders(request):
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    context = {'orders': orders}
    return render(request, 'orders.html', context)


@login_required
def order_details(request, id):
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    order_items = OrderProduct.objects.filter(order_id=id)
    context = {'order': order, 'orderitems': order_items}
    return render(request, 'order_details.html', context)


@login_required
def user_comments(request):
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id).order_by('-create_at')
    context = {'comments': comments, }

    return render(request, 'user_comments.html', context)
