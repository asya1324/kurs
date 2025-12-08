import csv, json
from bson import ObjectId

test_ids = {}
question_ids = {}

def load_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

# Load CSV
tests = load_csv("test.csv")
questions = load_csv("question.csv")
choices = load_csv("choice.csv")
results = load_csv("testresult.csv")

# Convert tests
tests_json = []
for row in tests:
    oid = ObjectId()
    test_ids[row["id"]] = oid
    tests_json.append({
        "_id": oid,
        "title": row["title"],
        "description": row["description"],
        "author_id": int(row["author_id"]),
        "is_published": row["is_published"] == "1"
    })

json.dump(tests_json, open("mongo_tests.json", "w"), indent=2, default=str)

# Convert questions
questions_json = []
for row in questions:
    oid = ObjectId()
    question_ids[row["id"]] = oid
    questions_json.append({
        "_id": oid,
        "test": test_ids[row["test_id"]],
        "text": row["text"],
        "qtype": row.get("qtype", "single")
    })

json.dump(questions_json, open("mongo_questions.json", "w"), indent=2, default=str)

# Convert choices
choices_json = []
for row in choices:
    choices_json.append({
        "_id": ObjectId(),
        "question": question_ids[row["question_id"]],
        "text": row["text"],
        "is_correct": row["is_correct"] == "1"
    })

json.dump(choices_json, open("mongo_choices.json", "w"), indent=2, default=str)

# Convert results
results_json = []
for row in results:
    results_json.append({
        "_id": ObjectId(),
        "user_id": int(row["user_id"]),
        "test": test_ids[row["test_id"]],
        "score": int(row["score"]),
        "total": int(row["total"]),
        "created_at": row["created_at"]
    })

json.dump(results_json, open("mongo_results.json", "w"), indent=2, default=str)
