from django import template
from django.utils.safestring import mark_safe
from mainapp.models import Menu

register = template.Library()
bold = "style='font-weight: bold;'"


@register.simple_tag(name="draw_menu", takes_context=True)
def draw_menu(context, menu_name):
    if active := context["request"].GET.get("active", None):
        active = int(active)
    if menu := (Menu.objects.filter(slug=menu_name)).first():
        content = f"""
        <h3>{menu.title}</h3>
        <ul>"""
        for x in menu.get_sorted(active):
            content += f'<li><a href="?active={x.id}" {bold if active == x.id else ""}>{x.indent_name}</a></li>'  # type: ignore  # noqa
        content += "</ul>"
        return mark_safe(content)
    return f"please be sure that you have a menu with the name \"{menu_name}\""
