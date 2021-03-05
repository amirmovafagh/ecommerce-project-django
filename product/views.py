from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from product.forms import CommentForm
from product.models import Category, Product, Gallery, Comment, Variants


def index(request, id, slug):
    comments = Comment.objects.filter(product_id=id, status='True')
    product = get_object_or_404(Product, slug=slug, status='True')
    # product = Product.objects.get(pk=id)
    images = Gallery.objects.filter(product_id=id)
    context = {
        'product': product,
        'images': images,
        'comments': comments}
    if product.variant != "None":  # there is variants
        if request.method == 'POST':
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw('SELECT * FROM product_variants WHERE product_id=%s GROUP BY size_id', [id])
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id)
            sizes = Variants.objects.raw('SELECT * FROM product_variants WHERE product_id=%s GROUP BY size_id', [id])
            variant = Variants.objects.get(id=variants[0].id)
        context.update({'sizes': sizes,
                        'colors': colors,
                        'variant': variant, })
    return render(request, 'product_detail.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {'size_id': size_id, 'productid': productid, 'colors': colors}
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


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
