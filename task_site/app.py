from flask import Flask, render_template, request, redirect

app = Flask(__name__)

tasks = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "task" in request.form:
            task = request.form["task"]
            if task:
                tasks.append(task)
        elif "remove" in request.form:
            index_to_remove = int(request.form["remove"])
            tasks.pop(index_to_remove)
        return redirect("/")
    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)