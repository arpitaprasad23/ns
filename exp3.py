import re

def check_password_strength(password):
    feedback = []

    if len(password) < 8:
        feedback.append("Password should be at least 8 characters long")

    if not re.search(r"[a-z]", password):
        feedback.append("Add lowercase letters")

    if not re.search(r"[A-Z]", password):
        feedback.append("Add uppercase letters")

    if not re.search(r"[0-9]", password):
        feedback.append("Include numbers")

    if not re.search(r"[!@#$%^&*]", password):
        feedback.append("Include special characters")

    if len(feedback) == 0:
        return "Strong Password 💪"
    else:
        return "Weak Password ❌\n" + "\n".join(feedback)


password = input("Enter your password: ")
print(check_password_strength(password))