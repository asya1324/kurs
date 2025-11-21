from django.urls import path
from . import views
from .views import home

urlpatterns = [
    path('login/', views.login, name='login'),
    path('home/', home, name='home'),
    path('tests/', views.tests, name='tests'),
    path('test/', views.test, name='test'),
    path('register/', views.register, name='register'),
    path("tests/<int:id>/", views.test_detail, name="test_detail"),
]

