import json
from datetime import datetime
import os

# Ensure the directory for the chat logs exists
os.makedirs("history", exist_ok=True)

def log_feedback(question, answer, label):
    """
    Logs the feedback into a JSON file.
    
    Parameters:
    - question (str): The question asked by the user.
    - answer (str): The answer provided by the assistant.
    - label (str): The feedback label (positive/negative).
    """
    entry = {
        "timestamp": str(datetime.now()),  # Current timestamp in string format
        "question": question,  # The question asked by the user
        "answer": answer,  # The assistant's response
        "feedback": label  # The feedback (positive or negative)
    }

    try:
        # Open the JSON file in append mode to add a new log entry
        with open("history/chat_logs.json", "a") as f:
            f.write(json.dumps(entry) + "\n")
    except IOError as e:
        # Handle any I/O errors that might occur while writing to the file
        print(f"Error while writing to chat_logs.json: {e}")
