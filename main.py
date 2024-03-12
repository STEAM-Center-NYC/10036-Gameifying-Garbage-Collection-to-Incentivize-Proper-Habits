from flask import Flask, render_template, request, redirect, g 
import flask_login 
import pymysql 
import pymysql.cursors 

app = Flask(__name__) 

def connect_db():
    return pymysql.connect(
        host= '10.100.33.60',
        user= 'mmcfowler',
        password= '220878185',
        database= 'mmcfowler_BinBuddy',
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
        
        
@app.route("/")
def index():
    return render_template('index.html.jinja')

@app.route("/rewards")
def rewards():
    return render_template('rewards.html.jinja')

