import random
import string
from sheets_helper import add_key_to_sheet

def generate_key(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def main():
    student_name = input("Enter student name: ").strip()

    if not student_name:
        print("Student name cannot be empty.")
        return

    new_key = generate_key()
    add_key_to_sheet(new_key, student_name)

    print(f"Key for {student_name}: {new_key}")

if __name__ == '__main__':
    main()
