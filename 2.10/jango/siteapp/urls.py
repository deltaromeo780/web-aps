from django.urls import path
from . import views

app_name = "siteapp"

urlpatterns = [
    path("", views.main, name="main"),
    path("load/", views.load, name="load"),
    path("author/<str:author_fullname>", views.author, name="author"),
    path("add_author/", views.add_author, name="add_author"),
    path("add_quote/", views.add_quote, name="add_quote"),
]
