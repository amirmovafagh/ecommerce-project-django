from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from order.forms import ShopCartForm
from order.models import ShopCart
from product.models import Category
from user.forms import EditProfileInfoForm, AddEditAddressForm
from user.models import UserProfile, UserAddress


def order(request):
    return HttpResponse(str("id"))


@login_required(login_url='/login')  # check login
def add_product(request, id):
    last_url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session Information

    if current_user.id is None:
        messages.warning(request, "لطفا وارد شوید.")
        return HttpResponseRedirect(last_url)
    check_product = ShopCart.objects.filter(product_id=id)  # check product in shopcart
    if check_product:
        control = True  # the product is in the cart
    else:
        control = False  # the product is not in the cart

    if request.method == 'POST':  # if there is a post request

        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control:  # Update shopCart
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else:  # Insert to shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
            messages.success(request, "محصول به سبد خرید افزوده شد.")
            return HttpResponseRedirect(last_url)
        # else:  # if there is no post
        #     if control:
        #         # Update shopCart
        #         data = ShopCart.objects.get(product_id=id)
        #         data.quantity += 1
        #         data.save()  # save data
        #     else:  # Insert to shopcart
        #         data = ShopCart()
        #         data.user_id = current_user.id
        #         data.product_id = id
        #         data.quantity = 1
        #         data.save()
        #     messages.success(request, "محصول به سبد خرید افزوده شد.")
        #     return HttpResponseRedirect(last_url)


def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    address = UserAddress.objects.filter(user_id=current_user.id)
    totalprice = 0
    for rs in shop_cart:
        totalprice += rs.product.price * rs.quantity
    context = {'shopcart': shop_cart,
               'category': category,
               'totalprice': totalprice,
               'address': address,

               }
    return render(request, 'shopcart_products.html', context)


@login_required(login_url='/login')  # check login
def remove_from_cart(request, id):
    ShopCart.objects.filter(id=id).delete()
    # messages.success(request, "از سبد خزید حذف شد.")
    return HttpResponseRedirect("/order/shopcart")


def order_products_address(request):
    if request.method == 'POST':
        current_user = request.user
        form = AddEditAddressForm(request.POST)
        print(request.POST.get('shipping'))
        messages.success(request, request.POST.get('shipping'))
        if form.is_valid():
            data = UserAddress()
            data.user_id = current_user.id
            data.firstname = form.cleaned_data.get('firstname')
            data.lastname = form.cleaned_data.get('lastname')
            data.phone = form.cleaned_data.get('phone')
            data.state = form.cleaned_data.get('state')
            data.city = form.cleaned_data.get('city')
            data.address = form.cleaned_data.get('address')
            data.postalcode = form.cleaned_data.get('postalcode')
            data.default_shipping_address = True
            data.save()
            messages.success(request, "آدرس شما اضافه شد.")
            return HttpResponseRedirect('/order/orderproduct')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/order/orderproduct')

    category = Category.objects.all()
    form = AddEditAddressForm()
    current_user = request.user
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    address = UserAddress.objects.filter(user_id=current_user.id)
    totalprice = 0
    for rs in shop_cart:
        totalprice += rs.product.price * rs.quantity
    context = {'shopcart': shop_cart,
               'category': category,
               'totalprice': totalprice,
               'address': address,
               'form': form
               }
    return render(request, 'order_product_address.html', context)


def order_checkPrice(request):
    return None


def payment_methods(request):
    category = Category.objects.all()
    current_user = request.user
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    address = UserAddress.objects.filter(user_id=current_user.id)
    totalprice = 0
    for rs in shop_cart:
        totalprice += rs.product.price * rs.quantity
    context = {'shopcart': shop_cart,
               'category': category,
               'totalprice': totalprice,
               'address': address,
               }
    return render(request, 'payment_methods.html', context)
