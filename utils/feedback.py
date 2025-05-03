import json
from datetime import datetime

def log_feedback(question, answer, label):
    entry = {
        "timestamp": str(datetime.now()),
        "question": question,
        "answer": answer,
        "feedback": label
    }
    with open("history/chat_logs.json", "a") as f:
        f.write(json.dumps(entry) + "\n")