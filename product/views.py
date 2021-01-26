from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.
from django.shortcuts import render, get_object_or_404

from product.forms import CommentForm
from product.models import Category, Product, Gallery, Comment


def index(request, id, slug):
    comments = Comment.objects.all()
    category = Category.objects.all()
    product = get_object_or_404(Product, slug=slug)
    images = Gallery.objects.filter(product_id=id)
    context = {'category': category, 'product': product, 'images': images, 'comments': comments}
    return render(request, 'product_detail.html', context)


def add_comment(request, id):
    last_url = request.META.get('HTTP_REFERER')  # get last url
    if request.method == 'POST':  # check the request was post
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()  # create relation with model
            data.subject = form.cleaned_data['subject']  # get form input
            data.rate = form.cleaned_data['rate']
            data.comment = form.cleaned_data['comment']
            data.product_id = id
            current_user = request.user.id
            data.user_id = current_user
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save to DB
            messages.success(request, "نظر شما ثبت شد.")
            return HttpResponseRedirect(last_url)
        else:
            messages.error(request, "لطفا اطلاعات را کامل وارد کنید.")

    return HttpResponseRedirect(last_url)
