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

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse


# ============ SIGN UP ============
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password")
        password2 = request.POST.get("password2")

        # error: password mismatch
        if password1 != password2:
            return render(request, "register.html", {"error": "Passwords do not match"})

        # error: username exists
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already taken"})

        # error: email exists
        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email already in use"})

        # create account
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        login(request, user)
        return redirect("home")

    return render(request, "register.html")


# ============ LOGIN ============
def simple_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")
        else:
            # return login error inside same page
            return render(request, "register.html", {"login_error": "Invalid username or password"})

    return HttpResponse("Invalid request")


# ============ LOGOUT ============
def simple_logout(request):
    logout(request)
    return redirect("home")


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



from django.shortcuts import render, redirect
from .models import Test
from django.contrib.auth.decorators import login_required

def test_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        # створюємо тест
        test = Test.objects.create(
            title=title,
            description=description,
            author=request.user,
            is_published=True
        )

        # ---- додаємо питання якщо введені (не обовʼязково) ----
        qtext = request.POST.get("qtext")
        opt1 = request.POST.get("opt1")
        opt2 = request.POST.get("opt2")
        opt3 = request.POST.get("opt3")
        opt4 = request.POST.get("opt4")
        correct = request.POST.get("correct")    # "0", "1", "2", "3"

        if qtext and opt1 and opt2 and opt3 and opt4 and correct is not None:
            q = Question.objects.create(test=test, text=qtext)

            options = [opt1, opt2, opt3, opt4]
            for idx, text in enumerate(options):
                Choice.objects.create(
                    question=q,
                    text=text,
                    is_correct=(idx == int(correct))
                )

        return redirect("tests")

    return render(request, "tests_create.html")




