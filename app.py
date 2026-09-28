"""
EASY Daily Task Manager
------------------------
The simplest possible version. No JavaScript fetch, no JSON API.
Every button is a plain HTML form. Every click reloads the page.

Python concepts used:
  - list        -> tasks = []
  - function     -> add_task(), delete_task(), toggle_task()
  - loop         -> for task in tasks
  - if / else    -> checking empty input, checking task["done"]
"""

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# -----------------------------------------
# Our "database" is just a plain Python list.
# Each task is a dictionary: {"id": 1, "title": "...", "done": False}
# -----------------------------------------
tasks = []
next_id = 1


# -----------------------------------------
# HOME PAGE - show all tasks
# -----------------------------------------
@app.route("/")
def home():
    error = request.args.get("error")   # will be None if no error

    # count tasks using a simple loop
    total = len(tasks)
    done_count = 0
    for t in tasks:
        if t["done"]:
            done_count = done_count + 1
    pending_count = total - done_count

    return render_template(
        "index.html",
        tasks=tasks,
        error=error,
        total=total,
        done_count=done_count,
        pending_count=pending_count,
    )


# -----------------------------------------
# ADD a new task
# -----------------------------------------
@app.route("/add", methods=["POST"])
def add():
    global next_id

    title = request.form.get("title", "")
    title = title.strip()   # remove extra spaces

    # ---- validation ----
    if title == "":
        return redirect("/?error=Please type a task before adding.")

    new_task = {"id": next_id, "title": title, "done": False}
    tasks.append(new_task)   # add to the list
    next_id = next_id + 1

    return redirect("/")


# -----------------------------------------
# DELETE one task by id
# -----------------------------------------
@app.route("/delete/<int:task_id>")
def delete(task_id):
    global tasks
    new_list = []
    for t in tasks:
        if t["id"] != task_id:
            new_list.append(t)
    tasks = new_list
    return redirect("/")


# -----------------------------------------
# TOGGLE a task between done / not done
# -----------------------------------------
@app.route("/toggle/<int:task_id>")
def toggle(task_id):
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = not t["done"]   # flip True/False
    return redirect("/")


# -----------------------------------------
# CLEAR every task
# -----------------------------------------
@app.route("/clear")
def clear():
    tasks.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
