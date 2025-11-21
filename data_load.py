from main.models import Test, Question, Choice
from django.contrib.auth import get_user_model


User = get_user_model()

author = User.objects.first()
if not author:
    print("No users found! Create a superuser first: python manage.py createsuperuser")
    exit()

test = Test.objects.create(
    title="SQL Basics Test",
    description="20 basic SQL questions",
    author=author,
    is_published=True
)

questions = [
    ("What does SQL stand for?",
     ["Structured Query Language", "Simple Query Logic", "Sequential Query Language", "Standard Question List"], 0),
    ("Which SQL statement is used to retrieve data from a database?",
     ["GET", "SELECT", "FETCH", "EXTRACT"], 1),
    ("What is a primary key?",
     ["A column that may have duplicate values", "A column that uniquely identifies each row and cannot be NULL",
      "A table index", "A foreign key from another table"], 1),
    ("Which command belongs to DDL?",
     ["INSERT", "UPDATE", "CREATE", "DELETE"], 2),
    ("What is the difference between WHERE and HAVING?",
     ["WHERE filters after grouping", "WHERE filters before aggregation", "Used only for INSERT", "No difference"], 1),
    ("What is a FOREIGN KEY?",
     ["Same table unique key", "References primary key of another table", "Used for indexing", "Can be NULL"], 1),
    ("Which JOIN returns all rows when matched in either table?",
     ["INNER JOIN", "LEFT JOIN", "FULL JOIN", "RIGHT JOIN"], 2),
    ("What is an INDEX in SQL?",
     ["A table", "Always NULL column", "Structure that increases query performance", "Stored procedure"], 2),
    ("What is a VIEW in SQL?",
     ["Materialised table", "Virtual table defined by SELECT", "Single column table", "Backup table"], 1),
    ("What is SQL injection?",
     ["Adding NULLs", "Deleting all tables", "Malicious SQL inserted into queries", "Optimising indexes"], 2),
    ("What is the difference between ROW_NUMBER(), RANK(), and DENSE_RANK()?",
     ["Same result", "Different ranking methods for ties", "Aggregate functions", "All skip ties"], 1),
    ("Which are SQL aggregate functions?",
     ["SUM()", "COUNT()", "LENGTH()", "AVG()"], [0, 1, 3]),
    ("Common SQL dialects?",
     ["Python, Java, C++", "MySQL, PostgreSQL, SQL Server, SQLite", "HTML, CSS, JS", "None"], 1),
    ("What is a subquery?",
     ["Query inside another query", "Type of index", "Backup", "Procedure"], 0),
    ("What is a stored procedure?",
     ["Stored outside DB", "Saved SQL code reusable", "Table for logins", "Non-updatable view"], 1),
    ("Purpose of CHECK constraint?",
     ["Allow NULL", "Enforce condition", "Auto index", "Drop table"], 1),
    ("Which modifies data?",
     ["CREATE TABLE", "DROP DB", "UPDATE", "GRANT"], 2),
    ("Which clause groups rows?",
     ["ORDER BY", "GROUP BY", "WHERE", "HAVING"], 1),
    ("Types of SQL subsets?",
     ["DDL", "DML", "DCL", "TDL"], [0, 1, 2]),
    ("Which changes table structure?",
     ["ALTER TABLE", "UPDATE TABLE", "MODIFY TABLE", "CHANGE TABLE"], 0),
]

for idx, (qtext, choices, correct) in enumerate(questions, start=1):
    qtype = "multi" if isinstance(correct, list) else "single"
    q = Question.objects.create(test=test, text=qtext, qtype=qtype)
    for i, ctext in enumerate(choices):
        is_correct = (i in correct) if isinstance(correct, list) else (i == correct)
        Choice.objects.create(question=q, text=ctext, is_correct=is_correct)


