from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from user.models import UserProfile, UserAddress, User


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'address', 'phone', 'city', 'state', 'postal_code',
                    'image_tag']


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'firstname', 'lastname', 'address', 'phone', 'city', 'state', 'postalcode',
                    'default_shipping_address']


UserAdmin.fieldsets[2][1]['fields'] = (
    'is_active', 'is_staff', 'is_superuser', 'is_author',
    'is_sales_manager', 'vip_user', 'groups', 'user_permissions')
UserAdmin.list_display += ('is_author',
                           'is_sales_manager', 'is_vip_user',)

admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
