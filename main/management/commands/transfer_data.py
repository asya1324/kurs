import pymysql
import pymysql.cursors
from mongoengine import connect, disconnect
from django.core.management.base import BaseCommand
from main.models import User, Test, Question, Choice, TestResult

class Command(BaseCommand):
    help = 'Transfers data from MariaDB/TiDB to MongoDB'

    def add_arguments(self, parser):
        parser.add_argument('--host', type=str, required=True, help='MariaDB Host')
        parser.add_argument('--user', type=str, required=True, help='MariaDB Username')
        parser.add_argument('--password', type=str, required=True, help='MariaDB Password')
        parser.add_argument('--db', type=str, required=True, help='MariaDB Database Name')
        parser.add_argument('--port', type=int, default=4000, help='MariaDB Port (default 4000 for TiDB)')
        # NEW ARGUMENT
        parser.add_argument('--mongo', type=str, required=True, help='MongoDB Connection String')

    def handle(self, *args, **options):
        # 1. Manually connect to MongoDB
        self.stdout.write(self.style.WARNING("Connecting to MongoDB..."))
        disconnect(alias='default') # Clear any failed previous attempts
        try:
            connect(host=options['mongo'], alias='default')
            self.stdout.write(self.style.SUCCESS("MongoDB Connected successfully!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"MongoDB Connection Failed: {e}"))
            return

        # 2. Connect to SQL
        self.stdout.write(self.style.WARNING(f"Connecting to SQL DB at {options['host']}..."))
        try:
            connection = pymysql.connect(
                host=options['host'],
                user=options['user'],
                password=options['password'],
                database=options['db'],
                port=options['port'],
                cursorclass=pymysql.cursors.DictCursor,
                ssl={'ca': '/etc/ssl/certs/ca-certificates.crt'} 
            )
        except pymysql.MySQLError as e:
            self.stdout.write(self.style.ERROR(f"SQL Connection failed: {e}"))
            self.stdout.write(self.style.ERROR("Tip: If running locally, remove the 'ssl' param in the script code if not needed."))
            return

        self.stdout.write(self.style.SUCCESS("SQL Connected! Transferring data..."))

        # Mappings to keep relationships intact (OldID -> NewMongoObject)
        user_map = {}
        test_map = {}
        question_map = {}

        try:
            with connection.cursor() as cursor:
                
                # 3. USERS
                self.stdout.write("Migrating Users...")
                cursor.execute("SELECT id, username, email, password, is_active FROM auth_user")
                for row in cursor.fetchall():
                    # Avoid duplicates
                    existing = User.objects(username=row['username']).first()
                    if existing:
                        user_map[row['id']] = existing
                        continue
                    
                    new_user = User(
                        username=row['username'],
                        email=row['email'],
                        password=row['password'], # Keep existing hash
                        is_active=bool(row['is_active'])
                    ).save()
                    user_map[row['id']] = new_user

                # 4. TESTS
                self.stdout.write("Migrating Tests...")
                cursor.execute("SELECT id, title, description, author_id, is_published FROM main_test")
                for row in cursor.fetchall():
                    author = user_map.get(row['author_id'])
                    author_id = str(author.id) if author else None
                    
                    new_test = Test(
                        title=row['title'],
                        description=row['description'],
                        author_id=author_id,
                        is_published=bool(row['is_published'])
                    ).save()
                    test_map[row['id']] = new_test

                # 5. QUESTIONS
                self.stdout.write("Migrating Questions...")
                cursor.execute("SELECT id, test_id, text, qtype FROM main_question")
                for row in cursor.fetchall():
                    test = test_map.get(row['test_id'])
                    if test:
                        q = Question(test=test, text=row['text'], qtype=row['qtype']).save()
                        question_map[row['id']] = q

                # 6. CHOICES
                self.stdout.write("Migrating Choices...")
                cursor.execute("SELECT question_id, text, is_correct FROM main_choice")
                for row in cursor.fetchall():
                    q = question_map.get(row['question_id'])
                    if q:
                        Choice(question=q, text=row['text'], is_correct=bool(row['is_correct'])).save()

                # 7. RESULTS
                self.stdout.write("Migrating Results...")
                cursor.execute("SELECT user_id, test_id, score, total FROM main_testresult")
                for row in cursor.fetchall():
                    u = user_map.get(row['user_id'])
                    t = test_map.get(row['test_id'])
                    if u and t:
                        TestResult(user=u, test=t, score=row['score'], total=row['total']).save()

        finally:
            connection.close()
            self.stdout.write(self.style.SUCCESS("Done! All data moved to MongoDB."))