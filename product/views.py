from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from product.models import Category, Product, Gallery, Variants


def index(request, id, slug):
    product = get_object_or_404(Product, slug=slug, status='True')
    # product = Product.objects.get(pk=id)
    images = Gallery.objects.filter(product_id=id)
    context = {
        'product': product,
        'images': images,}
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
