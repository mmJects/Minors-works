from flask import Blueprint,render_template,session,url_for,redirect,flash,request,jsonify
from .models import Notes,ToDos
from .support_for_todos import give_the_days_range
import json

acc = Blueprint("acc",__name__)

global todo

@acc.route("/<username>")
def acc_panel(username):
    if not session.get("Uid"):
        flash("Please login first to access this page..",category="warning")
        return redirect(url_for('auth.login'))
    name = session.get("name")
    if username != name:
        username = name
    return render_template("user_panel.html",username=username)

@acc.route("/<username>/notes",methods=['GET',"POST"])
def notes(username):
    note = Notes(uid=session["Uid"])
    notes = note.get_notes()
    # getting the username
    name = session.get("name")
    if username != name:
        username = name
    return render_template("notes.html",notes=notes,username=username)

@acc.route("/add-note",methods=["POST"])
def add_notes():
    if request.method == "POST":
        note = request.form.get("note").strip()
        if len(note) < 1:
            flash("Too short Note!!",category="error")
        else:
            new_note = Notes(note=note,uid=session["Uid"])
            new_note.insert_into_table()
    return redirect(url_for("acc.notes",username=session.get("name")))

@acc.route("/delete-note",methods=["POST"])
def delete_note():
    note_id = request.form.get("deleted-id")
    note = Notes(id=note_id,uid=session["Uid"])
    note.delete_note()
    return redirect(url_for("acc.notes",username=session.get("name")))

@acc.route("/<username>/to-dos",methods=["GET"])
def todos(username):
    global todo
    todo = ToDos(uid=session["Uid"])
    todos = todo.get_todos()
    name = session.get("name")
    if username != name:
        username = name
    date_range = give_the_days_range()
    return render_template("todo.html",todos=todos,date_range=date_range)

@acc.route("/add-todo",methods=["POST"])
def add_todos():
    if request.method == "POST":
        acti = request.form.get("activity")
        time = request.form.get("tm")
        day_difference = request.form.get("day_diff")
        full_timestamp = time + ":" + str(day_difference)
        todo.add_todos(acti,full_timestamp)
    return redirect(url_for("acc.todos",username=session.get("name")))

@acc.route("/delete-todo",methods=["POST"])
def delete_todo(auto=False):
    if request.method == "POST":
        if not auto:
            de_id = request.form.get("de")
        else:
            de_id = auto
        todo.delete_todos(de_id)
    return redirect(url_for("acc.todos",username=session.get("name")))

@acc.route("/auto-delete",methods=["POST"])
def auto_delete_todo():
    datas = json.loads(request.data)
    todoId = datas["ToDoId"]
    delete_todo(todoId)
    return jsonify({})


@acc.route("/delete-all/<item>")
def delete_all(item):
    if item == "notes":
        note = Notes(uid=session["Uid"])
        note.delete_note(all=True)
        return redirect(url_for("acc.notes",username=session.get("name")))
    else:
        todo.delete_todos(all_todos=True)
        return redirect(url_for("acc.todos",username=session.get("name")))

@acc.route("/search")
def search_todo():
    q = request.args.get("q")
    if q:
        result_dct = todo.search(q,session.get("Uid"))
    else:
        result_dct = {}
    print(result_dct)
    return jsonify(result_dct)


def page_not_found(error):
    return render_template('page_not_found.html'),404