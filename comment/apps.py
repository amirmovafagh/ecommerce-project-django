from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.db.models import signals


class CommentConfig(AppConfig):
    name = 'comment'
    verbose_name = 'نظر و دیدگاه\u200cها'

    def ready(self):
        import comment.signals

        signals.post_migrate.connect(comment.signals.create_permission_groups, sender=self)
        signals.post_migrate.connect(comment.signals.adjust_flagged_comments, sender=self)
