import json
import os.path
import random
import string

file_name = "storage.json"

def load_data():
    if not os.path.exists(file_name):
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump({"links": {}}, f, indent=4)

    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data: dict):
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def generate_code():
    characters = string.ascii_letters + string.digits
    new_code = ""
    for char in range(6):
        char = random.choice(characters)
        new_code += char
    return new_code

def add_link(long_url: str, user_id: int | str) -> str:
    data = load_data()
    links = data["links"]

    for code, info in links.items():
        if info["long_url"] == long_url and info["user_id"] == user_id:
            return code

    while True:
        code = generate_code()
        if code not in links:
            break

    links[code] = {"long_url": long_url, "user_id": user_id}
    save_data(data)
    return code

def resolve_code(code: str) -> str | None:
    data = load_data()
    info = data["links"].get(code)
    if not info:
        return None
    return info["long_url"]