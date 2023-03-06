from django.contrib import admin
from django.urls import path
from mainapp.views import renderer, get_menu_data

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", renderer, name="renderer"),
    path("get_menu_data/<slug:slug>/", get_menu_data, name="get_menu_data"),
]
