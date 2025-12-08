from django.urls import path
from main import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("tests/", views.tests, name="tests"),
    path("register/", views.register, name="register"),
    path("login/", views.simple_login, name="simple_login"),
    # Fix: Added the missing simple_logout pattern
    path("logout/", auth_views.LogoutView.as_view(next_page="index"), name="simple_logout"),
]