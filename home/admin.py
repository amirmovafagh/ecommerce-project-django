from django.contrib import admin

# Register your models here.
from home.forms import SliderImageValidForm, BannerImageValidForm
from home.models import Setting, ContactMessage, FAQ, SliderContent, BannerContent, BrandContent


class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'j_date', 'status']


class SliderContentAdmin(admin.ModelAdmin):
    form = SliderImageValidForm

    list_display = ['description', 'status', 'ordering_position', 'image_tag', ]


class BannerContentAdmin(admin.ModelAdmin):
    form = BannerImageValidForm
    list_display = ['description', 'status', 'ordering_position', 'image_tag', ]


class BrandContentAdmin(admin.ModelAdmin):
    list_display = ['description', 'status', 'ordering_position', 'image_tag', ]


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'j_date', 'status']
    list_filter = ['status']
    readonly_fields = ['name', 'subject', 'email', 'ip', 'message']


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'ordering_number', 'status']
    list_filter = ['status']


admin.site.register(Setting, SettingAdmin)
admin.site.register(SliderContent, SliderContentAdmin)
admin.site.register(BannerContent, BannerContentAdmin)
admin.site.register(BrandContent, BrandContentAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(FAQ, FAQAdmin)
