from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    BooleanField,
    ReferenceField,
    DateTimeField,
    EmailField,
    IntField,
)

class AnonymousUser:
    """
    A helper class to mock the Django AnonymousUser
    but for our Mongo setup.
    """
    is_authenticated = False
    username = ""
    id = None
    pk = None

class User(Document):
    username = StringField(required=True, unique=True, max_length=150)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)  # storing HMAC hash
    is_active = BooleanField(default=True)

    meta = {"collection": "users"}

    @property
    def is_authenticated(self):
        """Always return True for a valid user object."""
        return True

class Test(Document):
    title = StringField(required=True, max_length=200)
    description = StringField()
    author_id = StringField()
    is_published = BooleanField(default=True)

    meta = {"collection": "tests"}

    @property
    def questions(self):
        return Question.objects(test=self)

class Question(Document):
    test = ReferenceField(Test, required=True)
    text = StringField(required=True)
    qtype = StringField(default="single", max_length=10)

    meta = {"collection": "questions"}

    @property
    def choices(self):
        return Choice.objects(question=self)

class Choice(Document):
    question = ReferenceField(Question, required=True)
    text = StringField(required=True, max_length=300)
    is_correct = BooleanField(default=False)

    meta = {"collection": "choices"}

class TestResult(Document):
    user = ReferenceField(User, required=True)
    test = ReferenceField(Test, required=True)
    score = IntField(required=True)
    total = IntField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "test_results"}