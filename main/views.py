from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.hashers import make_password, check_password

# FIXED: Import from .models, not .mongo_models
from .models import User, Test, Question, Choice, TestResult


def get_current_user(request):
    uid = request.session.get("user_id")
    if not uid:
        return None
    try:
        return User.objects.get(id=uid)
    except User.DoesNotExist:
        return None


# ----------------- HOME -----------------

def home(request):
    return render(request, "home.html")


# ----------------- REGISTER -----------------

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "register.html", {"error": "Passwords do not match"})

        if User.objects(username=username).first():
            return render(request, "register.html", {"error": "Username already taken"})

        if User.objects(email=email).first():
            return render(request, "register.html", {"error": "Email already in use"})

        user = User(
            username=username,
            email=email,
            password=make_password(password1),
        ).save()

        request.session["user_id"] = str(user.id)
        return redirect("home")

    return render(request, "register.html")


# ----------------- LOGIN -----------------

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects(username=username).first()
        if user and check_password(password, user.password):
            request.session["user_id"] = str(user.id)
            return redirect("home")

        return render(
            request,
            "register.html",
            {"login_error": "Invalid username or password"},
        )

    # login form is inside register.html
    return redirect("register")


# ----------------- LOGOUT -----------------

def logout_view(request):
    request.session.flush()
    return redirect("home")


# ----------------- ALL TESTS -----------------

def tests(request):
    tests_qs = Test.objects.all()
    # We need to manually calculate question counts or pass a list of tuples
    # because 'test.questions' is a property method helper, not a direct field
    # But checking your template: {% for test, qcount in tests %}
    # This expects an iterable of tuples.
    
    data = []
    for t in tests_qs:
        # t.questions returns a QuerySet, so .count() works efficiently
        data.append((t, t.questions.count()))
        
    return render(request, "tests.html", {"tests": data})


# ----------------- TEST DETAIL / TAKE -----------------

def test_detail(request, id):
    user = get_current_user(request)
    if not user:
        return render(request, "login_required.html")

    try:
        test = Test.objects.get(id=id)
    except Test.DoesNotExist:
        raise Http404("Test not found")

    questions = list(test.questions)
    total = len(questions)
    score = None

    if request.method == "POST":
        score = 0
        for q in questions:
            field = f"q{q.id}"
            chosen_id = request.POST.get(field)
            if not chosen_id:
                continue
            try:
                chosen = Choice.objects.get(id=chosen_id)
            except Choice.DoesNotExist:
                continue
            if chosen.is_correct:
                score += 1

        TestResult(user=user, test=test, score=score, total=total).save()

        return render(
            request,
            "test_take.html",
            {"test": test, "score": score, "total": total},
        )

    return render(
        request,
        "test_take.html",
        {"test": test, "score": score, "total": total},
    )


# ----------------- CREATE TEST -----------------

def test_create(request):
    user = get_current_user(request)
    if not user:
        return render(request, "login_required.html")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        test = Test(
            title=title,
            description=description,
            author_id=str(user.id),
            is_published=True,
        ).save()

        qtext = request.POST.get("qtext")
        opt1 = request.POST.get("opt1")
        opt2 = request.POST.get("opt2")
        opt3 = request.POST.get("opt3")
        opt4 = request.POST.get("opt4")
        correct = request.POST.get("correct")

        # Basic validation
        if qtext and opt1 and opt2:
            q = Question(test=test, text=qtext).save()
            options = [opt1, opt2, opt3, opt4]
            # Filter out empty options if needed, but your form usually sends them empty
            
            for idx, text in enumerate(options):
                if text: # Only save non-empty options
                    Choice(
                        question=q,
                        text=text,
                        is_correct=(idx == int(correct)),
                    ).save()

        return redirect("tests")

    return render(request, "tests_create.html")


# ----------------- MY RESULTS -----------------

def my_tests(request):
    user = get_current_user(request)
    if not user:
        return render(request, "login_required.html")

    results = TestResult.objects(user=user).order_by("-created_at")
    return render(request, "my_tests.html", {"results": results})
