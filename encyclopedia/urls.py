from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),

    path("wiki/<str:atitle>", views.display_entry, name="entry"),

    path("create/", views.create_new_page, name="create"),
    path("save/", views.save_page, name="save"),

    path("edit/<str:atitle>", views.edit_page, name="edit"),
    path("savechanges/<str:atitle>", views.save_edit, name="save_edit"),

    path("random/", views.random_page, name="random"),
]
