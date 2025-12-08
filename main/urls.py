from django.urls import path
from main import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("tests/", views.tests, name="tests"),
    path("tests/create/", views.test_create, name="test_create"),
    path("tests/<str:id>/", views.test_detail, name="test_detail"),
    path("my-tests/", views.my_tests, name="my_tests"),
]

