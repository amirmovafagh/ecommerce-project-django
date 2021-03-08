import json

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from home.forms import ContactForm, SearchForm
from home.models import Setting, ContactMessage, FAQ
from product.models import Category, Product


def index(request):
    # category = Category.objects.all()
    products_slider = Product.objects.all().order_by('-id')[:3]  # show descending
    context = {'products_slider': products_slider}
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
        products = Product.objects.filter(category__slug=slug, status='True')
        return products

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug')
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=slug, status='True')
        return context


def search(request, page=1):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']  # get form input data
            catid = form.cleaned_data['catid']
            if catid == 0:
                products_list = Product.objects.filter(
                    title__icontains=query, status='True')  # select * FROM product WHERE title LIKE '%query'
                paginator = Paginator(products_list, 1)
                products = paginator.get_page(page)

            else:
                products_list = Product.objects.filter(
                    title__icontains=query, category_id=catid, status='True')
                paginator = Paginator(products_list, 1)
                products = paginator.get_page(page)
            context = {'products': products, 'query': query}
            return render(request, 'search_products.html', context)
    return HttpResponseRedirect('/')


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
