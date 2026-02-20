from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("shorten.html")

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        print(f"New message from {name}: {message}")
        return render_template("contact.html", success=True)
    return render_template("contact.html", success=False)

if __name__ == "__main__":
    app.run(debug=True)