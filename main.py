from flask import Flask, render_template, request, redirect, g, url_for
from pymysql.err import IntegrityError
from dynaconf import Dynaconf
import random
import os
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
        cursor.execute(
            "SELECT * FROM Users WHERE ID = %s AND Admin = 1",
            (flask_login.current_user.id,),
        )
        admin_user = cursor.fetchone()
        cursor.close()
        if admin_user:
            admin_access = True
    return render_template("index.html.jinja", admin_access=admin_access)


@app.route("/map")
def map_page():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM `Bins`")
    result = cursor.fetchall()
    return render_template("map.html.jinja", locations=result)


@app.route("/home", methods=["GET", "POST"])
def home():
    admin_access = False
    cursor = get_db().cursor()
    cursor.execute("SELECT Points FROM Users")
    points_dict = cursor.fetchone()
    points = points_dict['Points'] if points_dict else 0
    
    cursor.execute("SELECT * FROM Bins")
    all_bins_data = cursor.fetchall()
    
    bins_data = []
    while len(bins_data) < 5:
        random.shuffle(all_bins_data)
        bins_data = [bin_data for bin_data in all_bins_data if bin_data.get('SiteLocation') and bin_data['SiteLocation'].lower() != 'nan']

    bins_data = bins_data[:5]
    cursor.close()

    if flask_login.current_user.is_authenticated:
        cursor = get_db().cursor()
        cursor.execute(
            "SELECT * FROM Users WHERE ID = %s AND Admin = 1",
            (flask_login.current_user.id,),
        )
        admin_user = cursor.fetchone()
        cursor.close()
        if admin_user:
            admin_access = True

    return render_template("homepage.html.jinja", admin_access=admin_access, points=points, bins_data=bins_data)



@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            cursor = get_db().cursor()
            sql = "INSERT INTO Users (Username, Email, Password) VALUES (%s, %s, %s)"
            cursor.execute(sql, (username, email, password))
            get_db().commit()
            return redirect(url_for("signin"))
        except IntegrityError:
            error = "Username or email already exists"
            return render_template("signup.html.jinja", error=error)
        finally:
            cursor.close()
    return render_template("signup.html.jinja")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if flask_login.current_user.is_authenticated:
        return redirect("/home")
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
            return redirect(url_for("home"))
        else:
            error = "Invalid username or password"
            return render_template("signin.html.jinja", error=error)
    return render_template("signin.html.jinja")


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect("/")


@app.route("/rewards")
def rewards():
    return render_template("rewards.html.jinja")


@app.route("/profile", methods=["GET", "POST"])
@flask_login.login_required
def profile():
    if request.method == "POST":
        about_me = request.form.get("about_me")
        if about_me:
            cursor = get_db().cursor()
            cursor.execute("UPDATE Users SET About = %s WHERE ID = %s", (about_me, flask_login.current_user.id))
            get_db().commit()
            cursor.close()
            return redirect(url_for("profile"))
    cursor = get_db().cursor()
    cursor.execute("SELECT About FROM Users WHERE ID = %s", (flask_login.current_user.id,))
    user_data = cursor.fetchone()
    cursor.close()
    return render_template("profile.html.jinja", about=user_data["About"])



@app.route("/contact")
def contact():
    return render_template("contact.html.jinja")


@app.route("/Admin/Dashboard", methods=["GET"])
def Admin():
    cursor = get_db().cursor()
    cursor.execute("SELECT COUNT(ID) AS id_count FROM Users")
    id_count_row = cursor.fetchone()  
    cursor.close()
    id_count_value = id_count_row["id_count"]
    return render_template("AdminDashboard.html.jinja", id_count_value=id_count_value)