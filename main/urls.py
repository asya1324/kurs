from django.urls import path
from . import views
from .views import home

urlpatterns = [

    path("", views.home, name="home"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.simple_logout, name="logout"),

    path("tests/", views.tests, name="tests"),
    path("tests/create/", views.test_create, name="test_create"),
    path("tests/<int:id>/", views.test_detail, name="test_detail"),

    path("my-tests/", views.my_tests, name="my_tests"),


]


