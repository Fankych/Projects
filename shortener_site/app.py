from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form.get('link', None)
        if not long_url:
            print(long_url, "Failed")
            return redirect(url_for('index', fail=1))
        else:
            print(long_url, "success")
            return redirect(url_for('index', ok=1))
    ok = request.args.get("ok")
    fail = request.args.get("fail")
    return render_template('index.html', link="", ok=ok, fail=fail)

if __name__ == "__main__":
    app.run(debug=True)