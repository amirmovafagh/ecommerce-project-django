from django.contrib import admin

# Register your models here.
from order.models import ShopCart, OrderProduct, Order, Shipment


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'quantity', 'price', 'product_total_price']
    list_filter = ['user']


class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'status']


class OrderProductLine(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'price', 'quantity', 'amount')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "shipment":
            kwargs['queryset'] = Shipment.objects.filter(status=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ['first_name', 'last_name', 'phone', 'city', 'total', 'status', 'code', 'postalcode', 'j_date',
                    'is_order_pay_valid']
    list_filter = ['status']
    search_fields = ('code', 'phone')
    readonly_fields = ('shipment',
                       'user', 'first_name', 'last_name', 'address', 'state', 'city', 'phone', 'first_name',
                       'last_name', 'ip', 'total',
                       'postalcode')
    can_delete = False
    inlines = [OrderProductLine]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'price', 'quantity', 'amount']
    list_filter = ['user']


admin.site.register(ShopCart, ShopCartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Shipment, ShipmentAdmin)
