from django.urls import path

from . import views

app_name = "entry"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.title, name="title"),
    path("search/", views.search, name="search"),
    path("newpage/", views.new_page, name="new_page"),
    path("edit/", views.edit_page, name="edit_page"),
    path("save_edit/", views.save_edit, name="save_edit"),
    path("random/", views.random_choice, name="random")
]
