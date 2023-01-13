from flask import Blueprint,render_template,request,flash,redirect,url_for,session
from .models import User
from datetime import datetime

auth = Blueprint("auth",__name__)

@auth.route("/login",methods=["GET","POST"])
def login():
    if session.get("Uid"):
        flash("You need to log out first before switching account",category="error")
        return redirect(url_for('views.home'))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User(email=email,password=password)
        result = user.check_email()
        if result == True:
            session["Uid"] = user.db_datas[0]["Uid"]
            session["name"] = user.db_datas[0]["name"]
            flash("Your account is successfully logged in!!",category="success")
            return redirect(url_for('acc.acc_panel',username=user.db_datas[0]["name"]))
        else:
            flash(result,category="error") 
    return render_template("login.html")

@auth.route("/sign-up",methods=["GET","POST"])
def sign_up():
    if session.get("Uid"):
        flash("Make sure log out your account before creating another account!!!",category="error")
        return redirect(url_for('views.home'))
    if request.method == "POST":
        name = request.form.get("name").capitalize()
        email = request.form.get("email")
        password = request.form.get("password")
        con_pass = request.form.get("con-pass")
        if password != con_pass:
            flash("Sorry!Your confirmation password is not identical to the original one.",category="error")
        elif len(name) < 3:
            flash("For your security , we recommend to use your name with at least three characters",category="error")
        elif len(email) < 5:
            flash("Invalid Email address!!!!",category="error")
        else:
            now = datetime.now()
            uid = now.strftime("%m%d%Y") + name + now.strftime("%H%M%S")
            new_user = User(uid=uid,name=name,email=email,password=password)
            duplicate_check = new_user.insert_into_table()
            if duplicate_check:
                flash("Account created...",category="success")
                session["Uid"] = new_user.datas["uid"]
                session["name"] = name
                return redirect(url_for('acc.acc_panel',username=name))
            else:
                flash("Email already exists...",category="error")
    return render_template("signup.html")

@auth.route("/log-out")
def log_out():
    session["Uid"] = None
    session["name"] = None
    return redirect("/auth/login")