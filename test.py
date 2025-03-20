from werkzeug.security import generate_password_hash

hashed_password = generate_password_hash("hashme")
print(hashed_password)  # Output: Hashed string like '$pbkdf2-sha256$29000$...'
