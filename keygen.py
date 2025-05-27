import secrets
charset = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
secret_key = ''.join(secrets.choice(charset) for _ in range(50))
print(secret_key)
