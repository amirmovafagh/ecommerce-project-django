from django.contrib import admin

# Register your models here.
from user.models import UserProfile, UserAddress


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'address', 'phone', 'city', 'state', 'postal_code',
                    'image_tag']


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'firstname', 'lastname', 'address', 'phone', 'city', 'state', 'postalcode',
                    'default_shipping_address']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
