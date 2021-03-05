import admin_thumbnails
from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from product.models import Category, Product, Gallery, Comment, Color, Variants, Size


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status']
    list_filter = ['status', 'parent']


class CategoryAdminMp(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

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


class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'variant', 'status', 'image_tag']
    list_filter = ['status', 'category']
    readonly_fields = ('image_tag',)
    inlines = [ProductGalleryInLine,ProductVariantsInline]
    prepopulated_fields = {'slug': ('title',)}


@admin_thumbnails.thumbnail('image')
class ProductGallery(admin.ModelAdmin):
    list_display = ['title', 'product', 'image_tag', 'image_thumbnail']
    list_filter = ['product']
    readonly_fields = ('image_tag',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'user', 'status', 'j_date']
    list_filter = ['status']
    readonly_fields = ('user', 'product', 'subject', 'comment', 'rate', 'ip',)


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'color_tag']


class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'color', 'size', 'price', 'quantity', 'image_tag']


admin.site.register(Category, CategoryAdminMp)
admin.site.register(Product, ProductAdmin)
admin.site.register(Gallery, ProductGallery)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Variants, VariantsAdmin)
