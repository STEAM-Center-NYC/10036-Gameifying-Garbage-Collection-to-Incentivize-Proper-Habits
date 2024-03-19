from flask import Flask, render_template, request, redirect, g 
import flask_login 
import pymysql 
import pymysql.cursors 

app = Flask(__name__) 

def connect_db():
    return pymysql.connect(
        host= '',
        user= '',
        password= '',
        database= '',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit= True
    )

def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
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
    if flask_login.current_user.is_authenticated:
        return redirect("/homepage")
    else:
        return render_template('index.html.jinja')


@app.route("/homepage")
def homepage():
    return render_template("homepage.html.jinja")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if flask_login.current_user.is_authenticated:
        return redirect("/homepage")
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
