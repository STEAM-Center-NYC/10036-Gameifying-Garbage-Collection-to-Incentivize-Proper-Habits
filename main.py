from flask import Flask, render_template, request, redirect, g, url_for
from pymysql.err import IntegrityError
from dynaconf import Dynaconf
import flask_login
import pymysql
import pymysql.cursors

app = Flask(__name__)
settings = Dynaconf(settings_file=["settings.toml"])
app.secret_key = "eiewvrijvbeqdivjbnVQDKENWjneqwc"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User:
    is_authenticated = True
    is_anonymous = False
    is_active = True

    def __init__(self, id, username):
        self.username = username
        self.id = id

    def get_id(self):
        return str(self.id)


def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user=settings.db_user,
        password=settings.db_pass,
        database=settings.db_name,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def get_db():
    if not hasattr(g, "db"):
        g.db = connect_db()
    return g.db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "db"):
        g.db.close()


@login_manager.user_loader
def load_user(user_id):
    cursor = get_db().cursor()
    cursor.execute("SELECT * From Users WHERE ID = " + str(user_id))
    result = cursor.fetchone()
    get_db().commit()
    cursor.close()
    if result is None:
        return None
    return User(result["ID"], result["Username"])


@app.route("/")
def landing():
    admin_access = False
    if flask_login.current_user.is_authenticated:
        cursor = get_db().cursor()
        cursor.execute("SELECT * FROM Users WHERE ID = %s AND Admin = 1", (flask_login.current_user.id,))
        admin_user = cursor.fetchone()
        cursor.close()
        if admin_user:
            admin_access = True
    return render_template('index.html.jinja', admin_access=admin_access)



@app.route("/homepage")
def homepage():
    return render_template("homepage.html.jinja")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if flask_login.current_user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        identifier = request.form["identifier"]
        password = request.form["password"]
        cursor = get_db().cursor()
        sql = f"SELECT * FROM Users WHERE Username = '{identifier}' OR Email = '{identifier}'"
        cursor.execute(sql)
        user = cursor.fetchone()
        cursor.close()
        get_db().commit()
        if user and user["Password"] == password:
            user_obj = User(user["ID"], user["Username"])
            flask_login.login_user(user_obj)
            return redirect(url_for("homepage"))
        else:
            error = "Invalid username or password"
            return render_template("signin.html.jinja", error=error)
    return render_template("signin.html.jinja")

@app.route("/rewards")
def rewards():
    return render_template("rewards.html.jinja")

@app.route("/profile")
def profile():
    return render_template("profile.html.jinja")