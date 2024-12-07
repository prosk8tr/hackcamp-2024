import models
from flask import Flask, render_template, redirect, request, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db = models.DbConnect()

repo_compare = ["", ""]

@app.route('/')
def root():
    return redirect("/home")

@app.route('/home')
def home():
    return render_template("index.html")
    
@app.route('/page1', methods=['GET', 'POST'])
def page1():
    repos = db.fetch_all_repositories()
    selected_repo = ""
    #im so sorry
    if 'repo' in request.args:
        selected_repo=request.args['repo']
        repo_compare[0] = selected_repo
        #return redirect('/comparison')

    if request.method == 'POST':
        print(request.form['rep'])
        repo_compare[1] = request.form['rep']
        return redirect(url_for('comparison'))

    return render_template("page1.html", repos=repos)

@app.route('/comparison')
def comparison():
    return render_template("comparison.html", repos=repo_compare)

@app.route('/metrics')
def metrics():
    return render_template("metrics.html")
