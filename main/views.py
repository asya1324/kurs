from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

# Create your views here.


def login(request):
    return render(request, "main/login.html")


def home(request):
    return render(request, "main/home.html")


def tests(request):
    return render(request, "main/tests.html")


def test(request):
    return render(request, "main/test.html")

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'main/register_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'main/register.html', {'form': form})
