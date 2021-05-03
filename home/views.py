import json

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.views.generic import CreateView, ListView

from home.models import Setting, ContactMessage, FAQ, SliderContent
from product.models import Category, Product


def index(request):
    # category = Category.objects.all()
    slider_contents = SliderContent.objects.active().order_by('ordering_position')
    products_newest = Product.objects.active().order_by('-create_at')[:6]  # show descending

    context = {'products_newest': products_newest, 'slider_contents': slider_contents}
    return render(request, 'home/index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, }
    return render(request, 'about.html', context)


# def contact(request):
#     if request.method == 'POST':  # check the request was post
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             data = ContactMessage()  # create relation with model
#             data.name = form.cleaned_data['name']  # get form input
#             data.email = form.cleaned_data['email']
#             data.subject = form.cleaned_data['subject']
#             data.message = form.cleaned_data['message']
#             data.ip = request.META.get('REMOTE_ADDR')
#             data.save()  # save to DB
#             messages.success(request, "پیام شما ارسال شد.")
#             return HttpResponseRedirect('/contact')
#         else:
#             messages.error(request, "لطفا اطلاعات را کامل وارد کنید.")
#     else:
#         form = ContactForm()
#     context = {'contactForm': form, }
#     return render(request, 'contact.html', context)

class ContactUs(SuccessMessageMixin, CreateView):
    model = ContactMessage
    template_name = "contact.html"
    fields = ['name', 'email', 'subject', 'message', ]
    success_url = '/'
    success_message = "پیام شما ارسال شد."


# def category_products(request, id, slug, page=1):
#     products_list = Product.objects.filter(category_id=id,
#                                            status='True')  # get_object_or_404(Product, )  # just show enable products
#
#     paginator = Paginator(products_list, 20)
#     # page = request.GET.get("page")
#     products = paginator.get_page(page)
#     category_data = get_object_or_404(Category, pk=id)
#     context = {'products': products, 'category_data': category_data}
#     return render(request, 'category_products.html', context)

class CategoryProductsList(ListView):
    paginate_by = 20
    template_name = 'category_products.html'

    def get_queryset(self):
        slug = self.kwargs.get('slug')

        in_stock = self.request.GET.get('in_stock')
        sort_list = self.request.GET.get('sort_list')
        if in_stock is not None and sort_list is not None:
            # if '0' in sort_list and '1' in in_stock:  # پربازدیدترین ها و موجود
            #     last_month = datetime.today() - timedelta(days=30)
            #     products = Product.objects.active().annotate(
            #         count=Count('hits',
            #                     filter=Q(slug=slug) and Q(producthit__create_at__gt=last_month) and Q(amount__gt=0))
            #     ).order_by('-count', '-create_at')
            if '1' in sort_list and '1' in in_stock:  # جدیدترین و موجود
                products = Product.objects.filter(category__slug=slug, status='True', amount__gt=0).order_by(
                    '-create_at')
            elif '2' in sort_list and '1' in in_stock:  # کمترین قیمت و موجود
                products = Product.objects.filter(category__slug=slug, status='True', amount__gt=0).order_by('price')
            elif '3' in sort_list and '1' in in_stock:  # بیشترین قیمت و موجود
                products = Product.objects.filter(category__slug=slug, status='True', amount__gt=0).order_by('-price')
            else:
                products = Product.objects.filter(category__slug=slug, status='True')
                return products
        elif in_stock is not None and '1' in in_stock:  # فقط کالاهای موجود
            products = Product.objects.filter(category__slug=slug, status='True', amount__gt=0)
        # elif sort_list is not None and '0' in sort_list:  # فقط پربازدیدترین ها
        #     last_month = datetime.today() - timedelta(days=30)
        #     products = Product.objects.filter(status='True', slug=slug).annotate(
        #         count=Count('hits', Q(producthit__create_at__gt=last_month))
        #     ).order_by('-count', '-create_at')
        elif sort_list is not None and '1' in sort_list:  # فقط جدیدترین ها
            products = Product.objects.filter(category__slug=slug, status='True').order_by(
                '-create_at')
        elif sort_list is not None and '2' in sort_list:  # کمترین قیمت
            products = Product.objects.filter(category__slug=slug, status='True', ).order_by('price')
        elif sort_list is not None and '3' in sort_list:  # بیشترین قیمت
            products = Product.objects.filter(category__slug=slug, status='True', ).order_by('-price')
        else:
            products = Product.objects.filter(category__slug=slug, status='True')
        return products

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug')
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=slug, status='True')
        return context


def search(request, page=1):
    query = request.GET.get('q')
    if query:
        products_list = Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            status='True')  # select * FROM product WHERE title or description LIKE '%query'
        paginator = Paginator(products_list, 20)
        products = paginator.get_page(page)

        context = {'products': products, 'query': query}
        return render(request, 'search_products.html', context)
    else:
        last_url = request.META.get('HTTP_REFERER')  # get last url
        messages.warning(request, "لطفا عبارتی را برای جستجو وارد کنید")
        return HttpResponseRedirect(last_url)


def search_auto(request):
    if request.is_ajax():
        query = request.GET.get('term', '')
        print(query)
        products = Product.objects.filter(title__icontains=query)
        results = []
        for pr in products:
            product_json = {}
            product_json = pr.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def faq(request):
    faq = FAQ.objects.filter(status='True')
    context = {
        'faq': faq, }
    return render(request, 'home/faq.html', context)
