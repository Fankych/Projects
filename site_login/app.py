from datetime import timedelta
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "sheesh"
users = [
    {"login": "admin", "password": "admin"},
    {"login": "user", "password": "1234"},
    {"login": "test", "password": "qwerty"}
]

app.permanent_session_lifetime = timedelta(days=7)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        found_user = None
        for u in users:
            if u["login"].casefold() == login.casefold():
                found_user = u
                break

        if found_user and found_user["password"].casefold() == password.casefold():
            session.permanent = True
            session["user"] = found_user["login"]
            print(f"Logged in {login}!")
            return redirect("/home")
        else:
            print("Login failed")
            return render_template("index.html", fail=True, login=login)
    return render_template('index.html', fail=False)

@app.route("/home")
def home():
    user = session.get("user")
    if not user:
        return redirect("/")

    return render_template('home.html', user=user)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)