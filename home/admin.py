from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactMessage, FAQ


class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'update_at', 'status']


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'update_at', 'status']
    list_filter = ['status']
    readonly_fields = ['name', 'subject', 'email', 'ip', 'message']


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'ordering_number', 'status']
    list_filter = ['status']


admin.site.register(Setting, SettingAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(FAQ, FAQAdmin)
