import json
import os.path
from functools import wraps
from flask import redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

file_name = "users.json"

def load_user():
    if not os.path.exists(file_name):
        data = {"meta": {"next_user_id": 1},
                "users": {}}
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return data

    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)

def save_user(data: dict) -> None:
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def add_user(login: str, password: str) -> int | None:
    login = (login or "").strip()
    password = password or ""

    if not login or not password:
        return None
    data = load_user()
    data.setdefault("meta", {"next_user_id": 1})
    user = data["users"]

    key = login.casefold()
    if key in user:
        return None
    user_id = data["meta"]["next_user_id"]
    data["meta"]["next_user_id"] += 1

    user[key] = {
        "id": user_id,
        "login": login,
        "password_hash": generate_password_hash(password),
    }
    save_user(data)
    return user_id

def authenticate(login: str, password: str) -> dict | None: #Function of authentication
    login = (login or "").strip()
    password = password or ""
    data = load_user()
    user = data["users"]
    key = login.casefold()
    info = user.get(key)
    if not info:
        return None

    if check_password_hash(info["password_hash"], password):
        return {"login": info["login"], "user_id": info["id"]}
    return None

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = session.get("user")
        if not user:
            return redirect(url_for("index"))

        return func(*args, **kwargs)
    return wrapper