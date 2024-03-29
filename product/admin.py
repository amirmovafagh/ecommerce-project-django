import admin_thumbnails
from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin
from django.contrib import messages
from django.utils.translation import ngettext

from product.models import Category, Product, Gallery, Color, Variants, Size, IPAddress, Specifications, \
    SpecificationType
from user.models import User


def make_enable(modeladmin, request, queryset):
    updated = queryset.update(status='True')
    modeladmin.message_user(request, ngettext(
        '%d فیلد موردنظر فعال شد.',
        '%d فیلدهای موردنظر فعال شدند.',
        updated,
    ) % updated, messages.SUCCESS)


make_enable.short_description = "فعال سازی فیلد انتخاب شده"


def make_disable(modeladmin, request, queryset):
    updated = queryset.update(status='False')
    modeladmin.message_user(request, ngettext(
        '%d فیلد موردنظر غیرفعال شد.',
        '%d فیلد موردنظر غیرفعال شدند.',
        updated,
    ) % updated, messages.SUCCESS)


make_disable.short_description = "غیرفعال کردن فیلد انتخاب شده"


def make_cat_enable(modeladmin, request, queryset):
    updated = queryset.update(status=True)
    modeladmin.message_user(request, ngettext(
        '%d فیلد موردنظر فعال شد.',
        '%d فیلدهای موردنظر فعال شدند.',
        updated,
    ) % updated, messages.SUCCESS)


make_cat_enable.short_description = "فعال سازی فیلد انتخاب شده"


def make_cat_disable(modeladmin, request, queryset):
    updated = queryset.update(status=False)
    modeladmin.message_user(request, ngettext(
        '%d فیلد موردنظر غیرفعال شد.',
        '%d فیلد موردنظر غیرفعال شدند.',
        updated,
    ) % updated, messages.SUCCESS)


make_cat_disable.short_description = "غیرفعال کردن فیلد انتخاب شده"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status']
    list_filter = ['status', 'parent']
    actions = [make_cat_enable, make_cat_disable]


class CategoryAdminMp(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    actions = [make_cat_enable, make_cat_disable]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                                                Product,
                                                'category',
                                                'products_count',
                                                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count

    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count

    related_products_cumulative_count.short_description = 'Related products (in tree)'


@admin_thumbnails.thumbnail('image')
class ProductGalleryInLine(admin.TabularInline):
    model = Gallery
    readonly_fields = ('id',)
    extra = 1


class SpecificationsInLine(admin.TabularInline):
    model = Specifications
    extra = 1


class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True


class ProductAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "creator":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ['title', 'variant', 'category_to_str', 'status', 'image_tag']
    list_filter = ['status', 'category']
    readonly_fields = ('image_tag',)
    inlines = [ProductGalleryInLine, SpecificationsInLine, ProductVariantsInline]
    prepopulated_fields = {'slug': ('title',)}
    actions = [make_enable, make_disable]


@admin_thumbnails.thumbnail('image')
class ProductGallery(admin.ModelAdmin):
    list_display = ['title', 'product', 'image_tag', 'image_thumbnail']
    list_filter = ['product']
    readonly_fields = ('image_tag',)

    def has_module_permission(self, request):
        return False


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'color_tag']

    def has_module_permission(self, request):
        return False


class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

    def has_module_permission(self, request):
        return False


class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'color', 'size', 'price', 'quantity', 'image_tag']

    def has_module_permission(self, request):
        return False


class SpecificationTypeAdmin(admin.ModelAdmin):
    list_display = ['name', ]

    def has_module_permission(self, request):
        return False


class SpecificationsAdmin(admin.ModelAdmin):
    list_display = ['type', 'detail', ]

    def has_module_permission(self, request):
        return False


admin.site.register(Category, CategoryAdminMp)
admin.site.register(Product, ProductAdmin)
admin.site.register(Gallery, ProductGallery)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Variants, VariantsAdmin)
admin.site.register(SpecificationType, SpecificationTypeAdmin)
admin.site.register(Specifications, SpecificationsAdmin)
admin.site.register(IPAddress)
