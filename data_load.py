import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "itestoria.settings")
import django
django.setup()


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



test2 = Test.objects.create(
    title="Python Basics Test",
    description="20 Python beginner questions",
    author=author,
    is_published=True
)

questions2 = [

    # 1
    (
        "What is the output of the following code?\n\n"
        "listOne = [20, 40, 60, 80]\n"
        "listTwo = [20, 40, 60, 80]\n\n"
        "print(listOne == listTwo)\n"
        "print(listOne is listTwo)",
        ["True, True", "True, False", "False, True", "False, False"],
        1
    ),

    # 2
    (
        "Are the statements below true or false?\n"
        "- Strings are immutable in Python.\n"
        "- Every time we modify a string, Python creates a new one.",
        ["True", "False"],
        0
    ),

    # 3
    (
        "What is the output of the following code?\n\n"
        "p, q, r = 10, 20, 30\n"
        "print(p, q, r)",
        ["10 20", "10 20 30", "Error: invalid syntax"],
        1
    ),

    # 4
    (
        "What is the purpose of the pass statement in Python?",
        [
            "It acts as a comment.",
            "It skips the current iteration of a loop.",
            "It is a null operation; nothing happens when it executes.",
            "It terminates the program."
        ],
        2
    ),

    # 5
    (
        "What is the output of the following code?\n\n"
        "x = 10\n"
        "y = 3\n"
        "print(x % y)",
        ["3", "1", "0", "3.33"],
        1
    ),

    # 6
    (
        "What is the output of print(type([]))?",
        ["<class 'tuple'>", "<class 'list'>", "<class 'dict'>", "<class 'set'>"],
        1
    ),

    # 7
    (
        "Which of the following data types is mutable in Python?",
        ["int", "tuple", "str", "list"],
        3
    ),

    # 8
    (
        "What is the output of the following code?\n\n"
        "valueOne = 5 ** 2\n"
        "valueTwo = 5 ** 3\n"
        "print(valueOne)\n"
        "print(valueTwo)",
        ["10", "15", "25", "125", "Error"],
        3
    ),

    # 9
    (
        "What is the output of the following code?\n\n"
        "str = 'pynative'\n"
        "print(str[1:3])",
        ["py", "yn", "pyn", "yna"],
        1
    ),

    # 10
    (
        "What is the output of the following code?\n\n"
        "print('Python' + 'Quiz')",
        ["Python Quiz", "PythonQuiz", "Python+Quiz", "Error"],
        1
    ),

    # 11
    (
        "How do you get the current working directory in Python?",
        ["os.cwd()", "os.get_current_directory()", "os.getcwd()", "os.current_dir()"],
        2
    ),

    # 12
    (
        "Can we use the 'else' block for a for loop?",
        ["No", "Yes"],
        1
    ),

    # 13
    (
        "What is the output of print(bool(0))?",
        ["True", "False", "None", "Error"],
        1
    ),

    # 14
    (
        "What is the purpose of the super() function in Python classes?",
        [
            "To call a method in the current class.",
            "To define a static method.",
            "To refer to the parent or sibling class dynamically.",
            "To explicitly destroy an object."
        ],
        2
    ),

    # 15
    (
        "What is the output of the following code?\n\n"
        "sampleList = ['Jon', 'Kelly', 'Jessa']\n"
        "sampleList.append(2, 'Scott')\n"
        "print(sampleList)",
        [
            "The program executed with errors",
            "['Jon', 'Kelly', 'Scott', 'Jessa']",
            "['Jon', 'Kelly', 'Jessa', 'Scott']",
            "['Jon', 'Scott', 'Kelly', 'Jessa']"
        ],
        0
    ),

    # 16
    (
        "What is the output of the following code?\n\n"
        "sampleSet = {'Jodi', 'Eric', 'Garry'}\n"
        "sampleSet.add(1, 'Vicki')\n"
        "print(sampleSet)",
        [
            "{'Vicki', 'Jodi', 'Garry', 'Eric'}",
            "{'Jodi', 'Vicki', 'Garry', 'Eric'}",
            "The program executed with error"
        ],
        2
    ),

    # 17
    (
        "Which of the following is NOT a valid variable name in Python?",
        ["_my_variable", "myVariable", "2myvariable", "my_variable2"],
        2
    ),

    # 18
    (
        "Which of the following data types is mutable in Python?",
        ["int", "tuple", "str", "list"],
        3
    ),

    # 19
    (
        "What is the output of the following code?\n\n"
        "a = [1, 2, 3]\n"
        "b = a\n"
        "b.append(4)\n"
        "print(a)",
        ["[1, 2, 3]", "[1, 2, 3, 4]", "[4, 1, 2, 3]", "Error"],
        1
    ),

    # 20
    (
        "How do you add an element to the end of a list in Python?",
        ["list.add(element)", "list.insert(element)", "list.append(element)", "list.extend(element)"],
        2
    ),

    # 21
    (
        "What is the output of the following code?\n\n"
        "var = 'James Bond'\n"
        "print(var[2::-1])",
        ["Jam", "dno", "maJ", "dnoB semaJ"],
        2
    ),

    # 22
    (
        "What is a tuple in Python?",
        [
            "A mutable, ordered sequence of items.",
            "An immutable, ordered sequence of items.",
            "A mutable, unordered collection of unique items.",
            "An immutable, unordered collection of key-value pairs."
        ],
        1
    ),

    # 23
    (
        "What is the output of the following code?\n\n"
        "def calculate(num1, num2=4):\n"
        "    res = num1 * num2\n"
        "    print(res)\n\n"
        "calculate(5, 6)",
        ["20", "The program executed with errors", "30"],
        2
    ),

    # 24
    (
        "What is the output of print(10 // 3)?",
        ["3.333", "3", "4", "1"],
        1
    ),

    # 25
    (
        "What is the output of the following code?\n\n"
        "result = True and False\n"
        "print(result)",
        ["True", "False", "Error", "None"],
        1
    ),
]


for idx, (qtext, choices, correct) in enumerate(questions2, start=1):
    qtype = "multi" if isinstance(correct, list) else "single"
    q = Question.objects.create(test=test2, text=qtext, qtype=qtype)

    for i, ctext in enumerate(choices):
        is_correct = (i in correct) if isinstance(correct, list) else (i == correct)
        Choice.objects.create(question=q, text=ctext, is_correct=is_correct)

test3 = Test.objects.create(
    title="Beginner HTML Test",
    description="20 beginner-friendly HTML questions",
    author=author,
    is_published=True
)

questions3 = [

    # 1
    (
        "What are HTML tags?",
        [
            "Keywords inside angle brackets that describe content and structure.",
            "Python functions used to style output.",
            "Commands executed by the browser’s CPU.",
            "SQL statements for web pages."
        ],
        0
    ),

    # 2
    (
        "What’s the difference between HTML and HTML5?",
        [
            "HTML5 adds multimedia, semantic tags, <audio>, <video>, and new APIs.",
            "There is no difference.",
            "HTML5 removed <div> and <span>.",
            "HTML is newer than HTML5."
        ],
        0
    ),

    # 3
    (
        "Which of the following is a correct basic HTML document structure?",
        [
            "<!DOCTYPE html>, <html>, <head>, <body>",
            "<html>, <meta>, <div>",
            "<html>, <canvas>, <script>",
            "<doctype>, <style>, <footer>"
        ],
        0
    ),

    # 4
    (
        "What’s the difference between a tag and an element?",
        [
            "A tag = markup inside < >; an element = tag + content + attributes.",
            "There is no difference.",
            "A tag is only visible text.",
            "An element is always a closing tag."
        ],
        0
    ),

    # 5
    (
        "Which tag is used for the largest heading?",
        ["<h6>", "<heading>", "<h1>", "<title>"],
        2
    ),

    # 6
    (
        "Which HTML tag is used to create a paragraph?",
        ["<text>", "<para>", "<body>", "<p>"],
        3
    ),

    # 7
    (
        "Which tag is used to insert an image?",
        ["<img>", "<pic>", "<image>", "<src>"],
        0
    ),

    # 8
    (
        "Which attribute is required for <img>?",
        ["href", "src", "alt", "title"],
        1
    ),

    # 9
    (
        "Which element contains metadata such as title and character encoding?",
        ["<meta>", "<info>", "<head>", "<header>"],
        2
    ),

    # 10
    (
        "What does <!DOCTYPE html> do?",
        [
            "Marks the beginning of the CSS section.",
            "Tells the browser to render in HTML5 mode.",
            "Starts the JavaScript engine.",
            "Closes the document."
        ],
        1
    ),

    # 11
    (
        "Which HTML tag is used for clickable links?",
        ["<link>", "<url>", "<a>", "<href>"],
        2
    ),

    # 12
    (
        "Which tag is used for unordered lists?",
        ["<ol>", "<ul>", "<li>", "<list>"],
        1
    ),

    # 13
    (
        "Which HTML element is semantic?",
        ["<div>", "<header>", "<span>", "<b>"],
        1
    ),

    # 14
    (
        "Which input type was introduced in HTML5?",
        ["text", "password", "email", "radio"],
        2
    ),

    # 15
    (
        "What is the correct tag for inserting a line break?",
        ["<break>", "<lb>", "<br>", "<line>"],
        2
    ),

    # 16
    (
        "What does the <title> tag control?",
        [
            "The visible headline on the page.",
            "Text shown in the browser tab.",
            "The background color of the page.",
            "The footer text."
        ],
        1
    ),

    # 17
    (
        "Which HTML element is used to group block-level content?",
        ["<div>", "<span>", "<section>", "<group>"],
        0
    ),

    # 18
    (
        "Which HTML tag is used to display code snippets?",
        ["<script>", "<pre>", "<code>", "<cmd>"],
        2
    ),

    # 19
    (
        "Which API was introduced in HTML5?",
        ["Web Storage", "Flash API", "JavaFX API", "Silverlight API"],
        0
    ),

    # 20
    (
        "Which tag is used to embed audio in HTML5?",
        ["<sound>", "<audio>", "<music>", "<mp3>"],
        1
    ),
]


for idx, (qtext, choices, correct) in enumerate(questions3, start=1):
    qtype = "multi" if isinstance(correct, list) else "single"
    q = Question.objects.create(test=test3, text=qtext, qtype=qtype)

    for i, ctext in enumerate(choices):
        is_correct = (i in correct) if isinstance(correct, list) else (i == correct)
        Choice.objects.create(question=q, text=ctext, is_correct=is_correct)




