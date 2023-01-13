from website import create_app,create_databases
from flask_session import Session

# create flask app
app = create_app()

# create databases
create_databases()

# configure the flask seesion
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

if __name__ == "__main__":
    app.run(debug=True)