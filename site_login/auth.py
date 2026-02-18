from functools import wraps
from flask import redirect, session, url_for

users = [
    {"login": "admin", "password": "admin"},
    {"login": "user", "password": "1234"},
    {"login": "test", "password": "qwerty"}
]

def authenticate(login: str, password: str) -> str | None: #Function of authentication
    for u in users:
        if u["login"].casefold() == login.casefold():
            if u["password"].casefold() == password.casefold():
                return u["login"]
    return None

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = session.get("user")
        if not user:
            return redirect(url_for("index"))

        return func(*args, **kwargs)
    return wrapper