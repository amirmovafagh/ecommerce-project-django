from datetime import timedelta, datetime

from django import template
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q

from home.models import Setting
from order.models import ShopCart
from product.models import Category, Product

register = template.Library()


@register.filter(name='persian_int')
def persian_int(english_int):
    devanagari_nums = ('۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹')
    number = str(english_int)
    return ''.join(devanagari_nums[int(digit)] for digit in number)


@register.simple_tag
def categorylist():
    return Category.objects.filter(status=True)


@register.inclusion_tag("category_navbar.html")
def category_navbar():
    return {'category': Category.objects.filter(status='True', )}


@register.simple_tag
def website_info():
    if Setting.objects.exists():
        return Setting.objects.get(pk=1)
    return None


# @register.simple_tag
# def shopcart_count(userid):
#     return ShopCart.objects.count(user_id=userid)


@register.simple_tag
def shopcart_info(userid):
    return ShopCart.objects.filter(user_id=userid)


@register.inclusion_tag("adminlte/link.html")
def link(request, link_name, content):
    return {
        "request": request,
        "link_name": link_name,
        "link": "user:{}".format(link_name),
        "content": content,
    }


@register.inclusion_tag("link.html")
def linkp(request, link_name, content):
    return {
        "request": request,
        "link_name": link_name,
        "link": "{}".format(link_name),
        "content": content,
    }


@register.inclusion_tag("home/products_suggest.html")
def popular_products():
    last_month = datetime.today() - timedelta(days=30)
    return {
        "products": Product.objects.active().annotate(
            count=Count('hits', filter=Q(producthit__create_at__gt=last_month))
        ).order_by('-count', '-create_at')[:16],
        "title": "پربازدیدترین‌ها",
    }


@register.inclusion_tag("home/products_suggest.html")
def hot_products():
    last_month = datetime.today() - timedelta(days=30)
    content_type_id = ContentType.objects.get(app_label='product', model='product').id
    return {
        "products": Product.objects.active().annotate(
            count=Count('hits',
                        filter=Q(comments__posted__gt=last_month) and Q(comments__content_type_id=content_type_id))
        ).order_by('-count', '-create_at')[:16],
        "title": "محصولات داغ",
    }
