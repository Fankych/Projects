from datetime import timedelta
from flask import Flask, render_template, request, redirect, session, url_for
from auth import authenticate, login_required
from site_login.storage import add_link, resolve_code

app = Flask(__name__)
app.secret_key = "sheesh"
app.permanent_session_lifetime = timedelta(days=7)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        login = request.form.get("login")
        password = request.form.get("password")
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

@app.route("/shorten", methods=['GET', 'POST'])
@login_required
def shorten():
    if request.method == "POST":
        long_url = request.form.get('link')
        if not long_url:
            return redirect(url_for('shorten', fail=True))

        user_id = session.get("user")
        code = add_link(long_url, user_id)
        return redirect(url_for("shorten", code=code))

    code = request.args.get("code")
    fail = request.args.get("fail")
    short_url = None
    long_url = None

    if code:
        short_url = url_for("go", code=code, _external=True)
        long_url = resolve_code(code)

    return render_template(
        "shorten.html",
        fail=fail,
        code=code,
        short_url=short_url,
        long_url=long_url
    )

@app.route("/u/<code>")
def go(code):
    long_url = resolve_code(code)
    if not long_url:
        return "Not found", 404
    return redirect(long_url)

if __name__ == '__main__':
    app.run(debug=True)