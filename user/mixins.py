from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from product.models import Product


class FieldsMixin():
    """Verify that the current user is is_superuser."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ["creator", "category", "title", "keywords", "description", "image", "price",
                           "amount", "minamount", "variant",
                           "detail", "status", "slug", ]
        elif request.user.is_sales_manager:
            self.fields = ["category", "title", "keywords", "description", "image", "price",
                           "amount", "minamount", "variant",
                           "detail", "status", "slug", ]
        else:
            raise Http404("صفحه موردنظر در دسترس نیست.")
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.creator = self.request.user
            if not self.obj.status == 'True':
                self.obj.status = 'False'
        return super().form_valid(form)


class CreatorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        if product.creator == request.user and product.status in ['False'] or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("صفحه موردنظر در دسترس نیست.")


class SuperUserAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("صفحه موردنظر در دسترس نیست.")


class UserAuthenticatedAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("home:index"))
        else:
            return super().dispatch(request, *args, **kwargs)
