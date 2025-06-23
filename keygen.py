import secrets

# A secure set of characters for a Django SECRET_KEY
charset = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

# Generate a 50-character random string
secret_key = ''.join(secrets.choice(charset) for _ in range(50))

print(secret_key)
