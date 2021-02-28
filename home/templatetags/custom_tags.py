from django import template

from order.models import ShopCart
from product.models import Category

register = template.Library()


@register.filter(name='persian_int')
def persian_int(english_int):
    devanagari_nums = ('۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹')
    number = str(english_int)
    return ''.join(devanagari_nums[int(digit)] for digit in number)


@register.simple_tag
def categorylist():
    return Category.objects.all()


# @register.simple_tag
# def shopcart_count(userid):
#     return ShopCart.objects.count(user_id=userid)


@register.simple_tag
def shopcart_info(userid):
    return ShopCart.objects.filter(user_id=userid)
