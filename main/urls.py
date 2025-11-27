from django.urls import path
from . import views
from .views import home

urlpatterns = [
    path('home/', home, name='home'),
    path('tests/', views.tests, name='tests'),
    path('test/', views.test, name='test'),
    path("register/", views.register, name="register"),
    path("login/", views.simple_login, name="login"),
    path("logout/", views.simple_logout, name="logout"),
    path("tests/<int:id>/", views.test_detail, name="test_detail"),
    path("tests/create/", views.test_create, name="test_create"),

]

