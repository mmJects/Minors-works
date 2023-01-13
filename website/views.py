from flask import Blueprint,render_template
views = Blueprint("views",__name__)

@views.route("/")
def home():
    return render_template("home.html")

## Under this file , the features of the home page of the website will be added.