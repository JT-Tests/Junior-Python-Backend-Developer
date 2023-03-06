from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Menu


def renderer(request, *args, **kwargs):
    context = {
        "menu": Menu.objects.all()
    }
    return render(request, "mainapp/index.html", context)


def get_menu_data(request, slug):
    menu = get_object_or_404(Menu, slug=slug)

    return JsonResponse([
        [x.id, x.indent_name]  # type: ignore
        for x in menu.get_sorted_all()
    ], safe=False)
