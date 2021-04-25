from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext

from comment.models import Comment, Flag, FlagInstance, Reaction, ReactionInstance, Follower


def show_comment(modeladmin, request, queryset):
    updated = queryset.update(status=True)
    modeladmin.message_user(request, ngettext(
        '%d دیدگاه منتشر شد.',
        '%d دیدگاه ها منتشر شدند.',
        updated,
    ) % updated, messages.SUCCESS)


show_comment.short_description = "انتشار دیدگاه های انتخاب شده"


def hide_comment(modeladmin, request, queryset):
    updated = queryset.update(status=False)
    modeladmin.message_user(request, ngettext(
        '%d نمایش دیدگاه لغو گردید.',
        '%d نمای دیدگاه ها لغو شد.',
        updated,
    ) % updated, messages.SUCCESS)


hide_comment.short_description = "لغو انتشار دیدگاه های انتخاب شده"


class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'posted', 'edited', 'content_type', 'user', 'email', 'status', 'urlhash')
    search_fields = ('content',)
    actions = [show_comment, hide_comment]

    class Meta:
        model = Comment


class InlineReactionInstance(admin.TabularInline):
    model = ReactionInstance
    extra = 0
    readonly_fields = ['user', 'reaction', 'reaction_type', 'date_reacted']


class ReactionModelAdmin(admin.ModelAdmin):
    list_display = ('comment', 'likes', 'dislikes')
    readonly_fields = list_display
    search_fields = ('comment__content',)
    inlines = [InlineReactionInstance]


class InlineFlagInstance(admin.TabularInline):
    model = FlagInstance
    extra = 0
    readonly_fields = ['user', 'flag', 'reason', 'info', 'date_flagged']


class FlagModelAdmin(admin.ModelAdmin):
    list_display = ('comment', 'moderator', 'state', 'count', 'comment_author')
    readonly_fields = list_display
    search_fields = ('comment__content',)
    inlines = [InlineFlagInstance]

    def has_module_permission(self, request):
        return False


class FollowerModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'content_type', 'content_object')
    readonly_fields = list_display
    search_fields = ('email',)

    def has_module_permission(self, request):
        return False


admin.site.register(Comment, CommentModelAdmin)
admin.site.register(Reaction, ReactionModelAdmin)
admin.site.register(Flag, FlagModelAdmin)
admin.site.register(Follower, FollowerModelAdmin)
