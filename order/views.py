from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from order.forms import ShopCartForm
from order.models import ShopCart


def order(request):
    return HttpResponse(str("id"))


@login_required(login_url='/login')  # check login
def add_product(request, id):
    last_url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session Information

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
