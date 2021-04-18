from decouple import config
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from zeep import Client

from home.views import send_message
from order.models import Order

MERCHANT = config('MERCHANT')
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 100  # Toman / Required
orderId = 0
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09022021302'  # Optional
CallbackURL = 'http://127.0.0.1:8000/verify/'  # Important: need to edit for realy server.


def send_request(request, id):
    global orderId
    orderId = id

    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    print(result.Status)
    if result.Status == 100:
        order = get_object_or_404(Order, id=orderId, user=request.user)
        print(order.phone)
        type(order.phone)
        send_message(order.phone,
                     "سفارش " + str(
                         order.code) + " در وضعیت پرداخت قرار گرفت لطفا از طریق درگاه بانک خرید خود را تکمیل کنید." + "\n مبلغ سفارش: " + '{:7,.0f}'.format(
                         order.total) + " تومان")
        return HttpResponseRedirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))


def verify(request):
    if request.GET.get('Status') == 'OK':
        order = get_object_or_404(Order, id=orderId, user=request.user)
        order.status = "New"
        order.save()
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            messages.success(request,
                             "\nسفارش شما ثبت شد." + "سریال پرداخت:\n " + str(result.RefID) + "شماره سفارش:\n " + str(
                                 order.code))
            send_message(order.phone,
                         "سفارش شما ثبت شد." + " سریال پرداخت:\n " + str(result.RefID) + "شماره سفارش:\n " + str(
                             order.code))
            context = {'order': order, 'ref_id': result.RefID}
            return render(request, 'order_completed.html', context)
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')
