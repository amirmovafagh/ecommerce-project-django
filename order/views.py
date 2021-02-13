from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from order.forms import ShopCartForm
from order.models import ShopCart
from product.models import Category
from user.forms import EditProfileInfoForm
from user.models import UserProfile


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
    profile = UserProfile.objects.get(user_id=current_user.id)
    totalprice = 0
    for rs in shop_cart:
        totalprice += rs.product.price * rs.quantity
    context = {'shopcart': shop_cart,
               'category': category,
               'totalprice': totalprice,
               'profile': profile,
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
        form = EditProfileInfoForm(request.POST)
        if form.is_valid():
            data = UserProfile()
            if data.objects.get(id=current_user.id) :  # update the profile info
                data = data.objects.get(id=current_user.id)
            data.first_name = form.cleaned_data.get('firstname')
            data.last_name = form.cleaned_data.get('lastname')
            data.phone = form.cleaned_data.get('phone')
            data.state = form.cleaned_data.get('state')
            data.city = form.cleaned_data.get('city')
            data.address = form.cleaned_data.get('address')
            data.postal_code = form.cleaned_data.get('zipcode')
            data.save()
    category = Category.objects.all()
    current_user = request.user
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    totalprice = 0
    for rs in shop_cart:
        totalprice += rs.product.price * rs.quantity
    context = {'shopcart': shop_cart,
               'category': category,
               'totalprice': totalprice,
               'profile': profile,
               }
    return render(request, 'order_product_address.html', context)


def order_checkPrice(request):
    return None
