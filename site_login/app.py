from datetime import timedelta
from flask import Flask, render_template, request, redirect, session, url_for
from auth import authenticate, login_required

app = Flask(__name__)
app.secret_key = "sheesh"
app.permanent_session_lifetime = timedelta(days=7)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        user = authenticate(login, password)

        if user:
            session.permanent = True
            session["user"] = user
            print(f"Logged in {login}!")
            return redirect(url_for("home"))
        else:
            print("Login failed")
            return render_template("index.html", fail=True, login=login)
    return render_template('index.html', fail=False, login="")

@app.route("/home")
@login_required
def home():
    user = session.get("user")
    return render_template('home.html', user=user)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

@app.route("/profile")
@login_required
def profile():
    user = session.get("user")
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)