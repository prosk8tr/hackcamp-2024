import models
from flask import Flask, render_template, redirect, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db = models.db_connect()

repo_compare = ["", ""]

@app.route('/')
def root():
    return redirect("/home")

@app.route('/home')
def home():
    return render_template("index.html")
    
@app.route('/page1')
def page1():
    repos = db.fetch_all_repositories()
    selected_repo = ""
    #im so sorry
    if 'repo' in request.args:
        selected_repo=request.args['repo']
        repo_compare[0] = selected_repo
        #return redirect('/comparison')
    return render_template("page1.html", repos=repos, selected_repo=selected_repo)

@app.route('/comparison')
def comparison():
    return render_template("comparison.html")

@app.route('/metrics')
def metrics():
    return render_template("metrics.html")
