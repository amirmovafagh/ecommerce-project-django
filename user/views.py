from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .mixins import FieldsMixin, FormValidMixin, CreatorAccessMixin, SuperUserAccessMixin, UserAuthenticatedAccessMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, CreateView, DeleteView, DetailView
from extra_views import CreateWithInlinesView, InlineFormSetFactory, UpdateWithInlinesView

from order.models import Order, OrderProduct
from product.models import Comment, Product, Gallery, Variants

# Create your views here.
from user.forms import EditProfileForm, SignupForm, UpdateAddressForm
from user.models import UserProfile, User, UserAddress
from .tokens import account_activation_token


class ProfileEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = "edit_information.html"
    form_class = EditProfileForm
    success_url = reverse_lazy("user:profile")
    success_message = "اطلاعات بروز شد."

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(ProfileEdit, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


@login_required  # check login
def index(request):
    current_user = request.user
    last_order = Order.objects.filter(user_id=current_user.id).last()
    context = {'lastOrder': last_order}
    return render(request, "user_profile.html", context)


class Index(LoginRequiredMixin, ListView):
    model = Order
    template_name = "user_profile.html"

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id).order_by("-create_at")


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.is_sales_manager or user.is_author:
            return reverse_lazy("user:admin")
        else:
            return reverse_lazy("home:index")


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
            # userprofile = UserProfile.objects.get(user_id=current_user.id)
            # if userprofile.image:
            #     request.session['userimage'] = userprofile.image.url

            return HttpResponseRedirect(reverse_lazy('home:index'))
        else:
            messages.warning(request, "خطا در ورود !! نام کاربری یا رمز عبور اشتباه است.")
            return HttpResponseRedirect(reverse_lazy('login'))


class Signup(UserAuthenticatedAccessMixin, CreateView):
    form_class = SignupForm
    template_name = "signup.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی اکانت'
        message = render_to_string('activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        messages.success(self.request, 'لینک فعال سازی به ایمیل شما ارسال شد.')
        return HttpResponseRedirect(reverse_lazy("login"))


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('home')
        messages.success(request, 'حساب کاربری شما با موفقیت فعال شد.')
        return HttpResponseRedirect(reverse_lazy("home:index"))
    else:
        messages.warning(request, 'لینک فعال سازی منقصی شده است.')

        return HttpResponseRedirect(reverse_lazy("home:index"))


# def logout_func(request):
#     logout(request)
#     return HttpResponseRedirect("/")


# @login_required  # check login
# def edit_info_page(request):
#     if request.method == 'POST':
#         user_form = UserUpdateForm(request.POST, instance=request.user)
#         profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
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
#     profile_form = EditProfileForm(instance=request.user.userprofile)
#     context = {'profile_form': profile_form, 'user_form': user_form}
#     return render(request, "edit_information.html", context)


# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!!
#             messages.success(request, "رمز عبور تغییر یافت.")
#             return HttpResponseRedirect('/user')
#         else:
#             messages.error(request, 'خطا در تغییر رمز عبور.' + str(form.errors))
#             return HttpResponseRedirect('/user/changepassword')
#     else:
#
#         form = PasswordChangeForm(request.user)
#
#         return render(request, 'change_password.html', {'form': form, })

class AddressList(LoginRequiredMixin, ListView):
    template_name = "address.html"

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user).order_by("-default_shipping_address")


class AddressUpdate(LoginRequiredMixin, UpdateView):
    form_class = UpdateAddressForm
    template_name = "edit_address.html"
    success_message = "آدرس بروز شد."
    success_url = reverse_lazy("user:address")

    def get_object(self, **kwargs):
        return UserAddress.objects.get(user=self.request.user, pk=self.kwargs.get('id'))


def address_delete(request, id):
    last_url = request.META.get('HTTP_REFERER')  # get last url
    UserAddress.objects.filter(user=request.user, pk=id).delete()
    messages.success(request, "آدرس با موفقیت حذف شد.")
    return HttpResponseRedirect(last_url)


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
    order = get_object_or_404(Order, user_id=current_user.id, id=id)
    order_items = OrderProduct.objects.filter(order_id=id)
    context = {'order': order, 'orderitems': order_items}
    return render(request, 'order_details.html', context)


@login_required
def user_comments(request):
    current_user = request.user
    comments = Comment.objects.filter(user=current_user)
    context = {'comments': comments, }

    return render(request, 'user_comments.html', context)


class AdminProductList(LoginRequiredMixin, ListView):
    queryset = Product.objects.all().order_by('-create_at')
    template_name = "adminlte/products.html"


class GalleryInline(InlineFormSetFactory):
    model = Gallery
    fields = ["title",
              "image", ]


class VariantsInline(InlineFormSetFactory):
    model = Variants
    fields = [
        "title",
        "color",
        "size",
        "image_id",
        "quantity",
        "price",
    ]


class AdminProductCreate(LoginRequiredMixin, FieldsMixin, FormValidMixin, CreateWithInlinesView):
    model = Product
    inlines = [GalleryInline, VariantsInline]

    # fields = ["creator", "category", "title", "keywords", "description", "image", "price",
    #           "amount", "minamount", "variant",
    #           "detail", "status", "slug", ] use mixins alternative this fields for managing user mode
    template_name = "adminlte/product_create_update.html"


class AdminProductUpdate(LoginRequiredMixin, FieldsMixin, FormValidMixin, CreatorAccessMixin, UpdateWithInlinesView):
    model = Product
    inlines = [GalleryInline, VariantsInline]

    template_name = "adminlte/product_create_update.html"


class AdminProductDelete(SuperUserAccessMixin, DeleteView):
    model = Product
    template_name = "adminlte/product_confirm_delete.html"
    success_url = reverse_lazy("user:adminProducts")


@login_required
def admin_user(request):
    return render(request, 'adminlte/home.html')


@login_required
def admin_orders(request):
    return render(request, 'adminlte/orders.html')
