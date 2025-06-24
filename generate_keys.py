import json
import random
import string
from datetime import datetime

KEY_FILE = 'used_keys.json'

def generate_key(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def add_key(student_name):
    with open(KEY_FILE, 'r') as f:
        keys = json.load(f)

    new_key = generate_key()
    while new_key in keys:
        new_key = generate_key()  # Avoid duplicates

    keys[new_key] = {
        "status": "unused",
        "student_name": student_name,
        "issued_on": datetime.now().strftime("%Y-%m-%d")
    }

    with open(KEY_FILE, 'w') as f:
        json.dump(keys, f, indent=4)

    print(f"Key for {student_name}: {new_key}")

if __name__ == '__main__':
    student = input("Enter student name: ")
    add_key(student)
