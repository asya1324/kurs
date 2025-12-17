from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from bson import ObjectId
from mongoengine import connect, disconnect
import mongomock

from main.models import User, Test, Question, Choice, TestResult


# ----------------- BASE TEST CLASS -----------------

class BaseMongoTest(TestCase):
    """
    Base class to handle MongoDB setup and teardown.
    Inherits from TestCase (not SimpleTestCase) to allow access to the 
    SQL database used by Django's Auth/Session system.
    """
    def setUp(self):
        # 1. Disconnect from any existing connections (to avoid pollution)
        disconnect()
        # 2. Connect to a MOCK in-memory database
        # This is instant and requires 'pip install mongomock'
        connect('itestoria_test_db', mongo_client_class=mongomock.MongoClient, alias='default')
        
        self.client = Client()
        self._flush_db()

    def tearDown(self):
        self._flush_db()
        # 3. Disconnect after test to clean up
        disconnect()

    def _flush_db(self):
        """Helper to clear all collections."""
        # This requires an active connection, which setUp now provides
        TestResult.objects.all().delete()
        Choice.objects.all().delete()
        Question.objects.all().delete()
        Test.objects.all().delete()
        User.objects.all().delete()

    def create_user(self, username="testuser", email="test@example.com", password="password"):
        """Helper to create a user."""
        return User(
            username=username,
            email=email,
            password=make_password(password)
        ).save()


# ----------------- AUTHENTICATION TESTS -----------------

class AuthTests(BaseMongoTest):
    
    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_register_get_page(self):
        """Test accessing register page via GET."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_success(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "pass",
            "password2": "pass"
        }
        response = self.client.post(reverse('register'), data)
        # Should redirect to home on success
        self.assertRedirects(response, reverse('home'))
        
        # Verify user exists in Mongo
        user = User.objects(username="newuser").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "new@example.com")
        
        # Verify session was created
        self.assertEqual(self.client.session.get("user_id"), str(user.id))

    def test_register_password_mismatch(self):
        data = {
            "username": "mismatch",
            "email": "fail@example.com",
            "password": "pass",
            "password2": "wrong"
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        # Check for error context or content
        self.assertContains(response, "Passwords do not match")
        self.assertEqual(User.objects.count(), 0)

    def test_register_duplicate_username(self):
        self.create_user(username="existing")
        data = {
            "username": "existing",
            "email": "other@example.com",
            "password": "pass",
            "password2": "pass"
        }
        response = self.client.post(reverse('register'), data)
        self.assertContains(response, "Username already taken")

    def test_register_duplicate_email(self):
        self.create_user(email="existing@example.com")
        data = {
            "username": "other",
            "email": "existing@example.com",
            "password": "pass",
            "password2": "pass"
        }
        response = self.client.post(reverse('register'), data)
        self.assertContains(response, "Email already in use")

    def test_login_get_redirect(self):
        """Accessing login via GET should redirect to register (where the form lives)."""
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('register'))

    def test_login_success(self):
        user = self.create_user(username="loginuser", password="securepass")
        data = {
            "username": "loginuser",
            "password": "securepass"
        }
        response = self.client.post(reverse('login'), data)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(self.client.session.get("user_id"), str(user.id))

    def test_login_invalid_password(self):
        self.create_user(username="loginuser", password="securepass")
        data = {
            "username": "loginuser",
            "password": "wrongpassword"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")
        self.assertIsNone(self.client.session.get("user_id"))

    def test_logout(self):
        # Log in first
        user = self.create_user()
        session = self.client.session
        session["user_id"] = str(user.id)
        session.save()

        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))
        self.assertIsNone(self.client.session.get("user_id"))


# ----------------- TEST MANAGEMENT TESTS -----------------

class TestManagementTests(BaseMongoTest):

    def setUp(self):
        super().setUp()
        self.user = self.create_user()
        # Login
        session = self.client.session
        session["user_id"] = str(self.user.id)
        session.save()

    def test_tests_list_view_authenticated(self):
        # Create a dummy test
        Test(title="Sample Test", author_id=str(self.user.id)).save()
        response = self.client.get(reverse('tests'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Test")

    def test_tests_list_view_anonymous(self):
        """Tests list should be visible even if not logged in."""
        self.client.logout()
        Test(title="Public Test", author_id="unknown").save()
        response = self.client.get(reverse('tests'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Public Test")

    def test_create_test_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('test_create'))
        # Should render login required template
        self.assertTemplateUsed(response, 'login_required.html')

    def test_create_test_get_authenticated(self):
        """Ensure the create form loads correctly for logged in users."""
        response = self.client.get(reverse('test_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tests_create.html')

    def test_create_test_flow(self):
        data = {
            "title": "New Integration Test",
            "description": "Testing creation",
            "question_count": "1",
            "qtext_1": "What is 2+2?",
            "opt1_1": "3",
            "opt2_1": "4",
            "opt3_1": "5",
            "opt4_1": "6",
            "correct_1": "1" # Index 1 -> "4"
        }
        
        response = self.client.post(reverse('test_create'), data)
        self.assertRedirects(response, reverse('tests'))

        # Verify DB content
        test = Test.objects(title="New Integration Test").first()
        self.assertIsNotNone(test)
        self.assertEqual(test.description, "Testing creation")
        
        q = Question.objects(test=test).first()
        self.assertEqual(q.text, "What is 2+2?")
        
        choices = Choice.objects(question=q)
        self.assertEqual(choices.count(), 4)
        
        correct_choice = choices.filter(is_correct=True).first()
        self.assertEqual(correct_choice.text, "4")

    def test_create_test_skips_empty_options(self):
        """Ensure that if user leaves opt3/opt4 empty, they aren't saved."""
        data = {
            "title": "Empty Opts Test",
            "description": "Desc",
            "question_count": "1",
            "qtext_1": "Question?",
            "opt1_1": "Yes",
            "opt2_1": "No",
            "opt3_1": "",  # Empty
            "opt4_1": "",  # Empty
            "correct_1": "0"
        }
        self.client.post(reverse('test_create'), data)
        
        test = Test.objects(title="Empty Opts Test").first()
        q = Question.objects(test=test).first()
        # Should only have 2 choices
        self.assertEqual(Choice.objects(question=q).count(), 2)


# ----------------- TEST TAKING TESTS -----------------

class TestTakingTests(BaseMongoTest):

    def setUp(self):
        super().setUp()
        self.user = self.create_user()
        
        # Setup session for login
        session = self.client.session
        session["user_id"] = str(self.user.id)
        session.save()

        # Create a full test scenario manually
        self.test = Test(
            title="Math Test", 
            description="Simple", 
            author_id=str(self.user.id)
        ).save()

        # Q1
        self.q1 = Question(test=self.test, text="1+1?").save()
        self.c1_wrong = Choice(question=self.q1, text="3", is_correct=False).save()
        self.c1_correct = Choice(question=self.q1, text="2", is_correct=True).save()

        # Q2
        self.q2 = Question(test=self.test, text="2+2?").save()
        self.c2_correct = Choice(question=self.q2, text="4", is_correct=True).save()
        self.c2_wrong = Choice(question=self.q2, text="5", is_correct=False).save()

    def test_view_test_detail_authenticated(self):
        url = reverse('test_detail', args=[str(self.test.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Math Test")
        self.assertContains(response, "1+1?")

    def test_view_test_detail_unauthenticated(self):
        self.client.logout()
        url = reverse('test_detail', args=[str(self.test.id)])
        response = self.client.get(url)
        # Should render login_required.html, not redirect
        self.assertTemplateUsed(response, "login_required.html")

    def test_view_test_detail_404(self):
        """Test accessing a non-existent test ID."""
        # Create a valid ObjectId that definitely doesn't exist
        fake_id = str(ObjectId()) 
        url = reverse('test_detail', args=[fake_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_submit_test_perfect_score(self):
        url = reverse('test_detail', args=[str(self.test.id)])
        
        data = {
            f"q{self.q1.id}": str(self.c1_correct.id),
            f"q{self.q2.id}": str(self.c2_correct.id),
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        
        # Check context for score
        self.assertEqual(response.context['score'], 2)
        self.assertEqual(response.context['total'], 2)
        
        # Verify Result Saved in DB
        result = TestResult.objects(user=self.user, test=self.test).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.score, 2)

    def test_submit_test_partial_score(self):
        url = reverse('test_detail', args=[str(self.test.id)])
        
        data = {
            f"q{self.q1.id}": str(self.c1_correct.id), # Correct
            f"q{self.q2.id}": str(self.c2_wrong.id),   # Wrong
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.context['score'], 1)
        
        result = TestResult.objects.first()
        self.assertEqual(result.score, 1)

    def test_submit_test_invalid_choice_id(self):
        """
        Submitting a choice ID that does not exist should not crash.
        The view logic wraps Choice.objects.get in try/except.
        """
        url = reverse('test_detail', args=[str(self.test.id)])
        fake_choice_id = str(ObjectId())

        data = {
            f"q{self.q1.id}": fake_choice_id,
            f"q{self.q2.id}": str(self.c2_correct.id), # One valid
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        
        # Score should be 1 (because one answer was valid/correct, the other was ignored)
        self.assertEqual(response.context['score'], 1)

    def test_my_results_view_authenticated(self):
        # Create a result manually
        TestResult(
            user=self.user, 
            test=self.test, 
            score=10, 
            total=10
        ).save()

        response = self.client.get(reverse('my_tests'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "10/10")
        self.assertContains(response, "Math Test")

    def test_my_results_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('my_tests'))
        self.assertTemplateUsed(response, "login_required.html")