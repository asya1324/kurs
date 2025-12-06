from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib.auth.models import User
from .models import Test, Question, Choice
from .models import TestResult


# ===================== HOME =====================

def home(request):
    return render(request, "home.html")


# ===================== LOGIN PAGE =====================

def login_page(request):
    return render(request, "register.html")


# ===================== REGISTER =====================

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "register.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already taken"})

        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email already in use"})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        django_login(request, user)
        return redirect("home")

    return render(request, "register.html")


# ===================== LOGIN LOGIC =====================

def simple_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            django_login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

    # GET → просто повертаємо сторінку логіну
    return render(request, "login.html")


# ===================== LOGOUT =====================

def simple_logout(request):
    logout(request)
    return redirect("home")


# ===================== VIEW ALL TESTS =====================

def tests(request):
    tests = Test.objects.all()
    return render(request, "tests.html", {"tests": tests})


# ===================== VIEW ONLY USER TESTS =====================

def my_tests(request):
    if not request.user.is_authenticated:
        return render(request, "login_required.html")

    tests = Test.objects.filter(author=request.user)
    return render(request, "my_tests.html", {"tests": tests})


# ===================== TAKE TEST (DETAIL + ANSWER FORM) =====================

def test_detail(request, id):
    if not request.user.is_authenticated:
        return render(request, "login_required.html")

    test = get_object_or_404(Test, id=id)

    total = test.questions.count()
    score = None  # значення за замовчуванням

    if request.method == "POST":
        score = 0
        for q in test.questions.all():
            field = f"q{q.id}"
            chosen_id = request.POST.get(field)

            if chosen_id:
                chosen = Choice.objects.get(id=chosen_id)
                if chosen.is_correct:
                    score += 1

        # ЗБЕРІГАЄМО РЕЗУЛЬТАТ
        TestResult.objects.create(
            user=request.user,
            test=test,
            score=score,
            total=total
        )

        return render(
            request,
            "test_take.html",
            {"test": test, "score": score, "total": total}
        )

    # GET запит (просто відкрити тест)
    return render(
        request,
        "test_take.html",
        {"test": test, "score": score, "total": total}
    )


# ===================== CREATE NEW TEST =====================

def test_create(request):
    if not request.user.is_authenticated:
        return render(request, "login_required.html")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        test = Test.objects.create(
            title=title,
            description=description,
            author=request.user,
            is_published=True
        )

        # Optional: Add question instantly (not required)
        qtext = request.POST.get("qtext")
        opt1 = request.POST.get("opt1")
        opt2 = request.POST.get("opt2")
        opt3 = request.POST.get("opt3")
        opt4 = request.POST.get("opt4")
        correct = request.POST.get("correct")

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



def my_tests(request):
    if not request.user.is_authenticated:
        return render(request, "login_required.html")

    results = TestResult.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "my_tests.html", {"results": results})



