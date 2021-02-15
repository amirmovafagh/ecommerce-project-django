from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from order.forms import ShopCartForm, OrderForm
from order.models import ShopCart, Order, OrderProduct
from product.models import Category, Product
from user.forms import EditProfileInfoForm, UpdateAddressForm
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
    addresses = UserAddress.objects.filter(user_id=current_user.id)
    totalprice = 0
    for rs in shop_cart:
        totalprice += rs.product.price * rs.quantity
    context = {'shopcart': shop_cart,
               'category': category,
               'totalprice': totalprice,
               'addresses': addresses,

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
        form = UpdateAddressForm(request.POST)
        address_state = request.POST.get('shipping')
        if address_state == 'addNewShippingAddress':  # add new address
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
                data.default_shipping_address = False
                data.save()
                messages.success(request, "آدرس شما اضافه شد.")
                return HttpResponseRedirect('/order/orderproduct')
            else:
                messages.warning(request, form.errors)
                return HttpResponseRedirect('/order/orderproduct')
        else:  # set selected address to default address
            addresses = UserAddress.objects.filter(user_id=current_user.id)
            for ad in addresses:
                if ad.id == int(address_state):
                    ad.default_shipping_address = True
                else:
                    ad.default_shipping_address = False
                ad.save()

            return HttpResponseRedirect('/order/paymentmethods')

    category = Category.objects.all()
    form = UpdateAddressForm()
    current_user = request.user
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    addresses = UserAddress.objects.filter(user_id=current_user.id)
    totalprice = 0
    for rs in shop_cart:
        totalprice += rs.product.price * rs.quantity
    context = {'shopcart': shop_cart,
               'category': category,
               'totalprice': totalprice,
               'addresses': addresses,
               'form': form
               }
    return render(request, 'order_product_address.html', context)


def order_check_price(request):
    return None


def payment_methods(request):
    category = Category.objects.all()
    current_user = request.user
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    addresses = UserAddress.objects.filter(user_id=current_user.id)
    totalprice = 0
    for rs in shop_cart:
        totalprice += rs.product.price * rs.quantity
    if request.method == 'POST':
        form = OrderForm(request.POST)
        current_user = request.user
        address = UserAddress.objects.get(default_shipping_address=True, user_id=current_user.id)
        print(address.firstname)
        if form.is_valid():
            data = Order()
            data.user_id = current_user.id
            data.first_name = address.firstname
            data.last_name = address.lastname
            data.address = address.address
            data.city = address.city
            data.state = address.state
            data.phone = address.phone
            data.postalcode = address.postalcode
            data.total = totalprice
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(6).upper()
            data.code = ordercode  # Random code
            data.save()

            # move shopcart items to order products
            for rs in shop_cart:
                detail = OrderProduct()
                detail.order_id = data.id  # order id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.product_total_price
                detail.save()

                # reduce quntity of sold product from Amount of product
                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()

            ShopCart.objects.filter(user_id=current_user.id).delete()  # clear & delete shopcart
            request.session['cart_items'] = 0
            messages.success(request, "سفارش شما ثبت شد.")
            return render(request, 'order_completed.html', {'ordercode': ordercode,'category':category})
        else:
            messages.warning(request, form.errors)

        return HttpResponseRedirect('/order/paymentmethods')

    context = {'shopcart': shop_cart,
               'category': category,
               'totalprice': totalprice,
               'addresses': addresses,
               }
    return render(request, 'payment_methods.html', context)
