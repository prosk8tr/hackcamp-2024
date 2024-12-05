import models
from flask import Flask, render_template, redirect
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db = models.db_connect()

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
