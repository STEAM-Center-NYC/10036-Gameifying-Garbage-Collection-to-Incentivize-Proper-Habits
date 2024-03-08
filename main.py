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