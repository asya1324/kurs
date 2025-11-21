from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Test, Question, Choice

# Create your views here.


def login(request):
    return render(request, "login.html")

def home(request):
    return render(request, 'home.html')

def tests(request):
    tests = Test.objects.all()
    return render(request, "tests.html", {"tests": tests})


def test(request):
    return render(request, "test.html")

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def simple_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")  
        else:
            return HttpResponse("Невірний логін або пароль")

    return HttpResponse("Invalid request")

def test_detail(request, id):
    test = get_object_or_404(Test, id=id)

    score = None
    total = test.questions.count()

    if request.method == "POST":
        score = 0

        for q in test.questions.all():
            field = f"q{q.id}"
            chosen_id = request.POST.get(field)

            if chosen_id:
                chosen = Choice.objects.get(id=chosen_id)
                if chosen.is_correct:
                    score += 1

    return render(
        request,
        "test_take.html",
        {
            "test": test,
            "score": score,  
            "total": total,
        }
    )






