import db_connection
from flask import Flask, render_template, redirect

app = Flask(__name__)

db = db_connection.db_connect()

@app.route('/')
def root():
    return redirect("/home")

@app.route('/home')
def home():
    return render_template("index.html")
    
@app.route('/page1')
def page1():
    return render_template("page1.html")

@app.route('/comparison')
def comparison():
    return render_template("comparison.html")