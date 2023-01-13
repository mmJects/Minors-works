import os
from flask import Flask
from cs50 import SQL

db = SQL("mysql://root:YES@localhost:3306/db_for_flask")

json_data_filepath = os.path.join(os.path.dirname(__file__),"static\datas\data.json")

def create_app():

    app = Flask(__name__)
    app.config["SECRET_KEY"] ="qazxswedcvfrtgbnhyujm1232"
    

    from .views import views
    from .auth import auth
    from .acc import acc,page_not_found

    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/auth/")
    app.register_blueprint(acc,url_prefix="/account/")
    app.register_error_handler(404,page_not_found)

    return app

def create_databases():
    query_user = """
        create table if not exists user_signup_data(
            Uid varchar(255) not null primary key,
            name varchar(255),
            email varchar(255) unique,
            pw varchar(255) not null,
            created_at timestamp default current_timestamp
        )
    """
    db.execute(query_user)
    query_notes = """
        create table if not exists users_notes(
            id int not null primary key auto_increment,
            note mediumtext,
            Uid varchar(255),
            foreign key (Uid) references user_signup_data(Uid)
        )
    """
    db.execute(query_notes)