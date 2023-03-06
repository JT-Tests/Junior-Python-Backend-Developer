from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Menu, Tree
from .forms import TreeForm

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ("indent_name",)
    change_form_template = "admin/tree_change_form.html"
    change_list_template = "admin/tree_list_form.html"
    list_filter = ("menu",)
    form = TreeForm

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['Menu'] = Menu.objects.all()  # type: ignore
        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        query = self.model.get_sorted()
        return query
