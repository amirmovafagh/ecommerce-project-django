from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from product.models import Category, Product, Gallery, Comment


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


class ProductGalleryInLine(admin.TabularInline):
    model = Gallery
    extra = 5


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'image_tag']
    list_filter = ['status', 'category']
    readonly_fields = ('image_tag',)
    inlines = [ProductGalleryInLine]
    prepopulated_fields = {'slug': ('title',)}


class ProductGallery(admin.ModelAdmin):
    list_display = ['title', 'product', 'image_tag']
    list_filter = ['product']
    readonly_fields = ('image_tag',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'user', 'status', 'create_at']
    list_filter = ['status']
    readonly_fields = ('user', 'product', 'subject', 'comment', 'rate', 'ip',)


admin.site.register(Category, CategoryAdminMp)
admin.site.register(Product, ProductAdmin)
admin.site.register(Gallery, ProductGallery)
admin.site.register(Comment, CommentAdmin)
