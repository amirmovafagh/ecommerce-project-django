from django.contrib import admin

# Register your models here.
from order.models import ShopCart, OrderProduct, Order


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'quantity', 'price', 'product_total_price']
    list_filter = ['user']


class OrderProductLine(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'price', 'quantity', 'amount')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'city', 'total', 'status', 'code', 'postalcode', 'j_date']
    list_filter = ['status']
    search_fields = ('code', 'phone')
    ordering = ['status', '-create_at']
    readonly_fields = (
        'first_name', 'last_name', 'address', 'state', 'city', 'phone', 'first_name', 'last_name', 'ip', 'total',
        'postalcode')
    can_delete = False
    inlines = [OrderProductLine]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'price', 'quantity', 'amount']
    list_filter = ['user']


admin.site.register(ShopCart, ShopCartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
