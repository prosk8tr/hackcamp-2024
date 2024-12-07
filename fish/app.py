import models
from flask import Flask, render_template, redirect, request, url_for
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

db = models.DbConnect()
graph_drawer = models.GraphDrawer()

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
    return render_template("page1.html", repos=repos)

@app.route('/comparison')
def comparison():
    return render_template("comparison.html", repos=repo_compare) #TODO: fix comparison.html, it doesn't inherit from template.html for some reason

@app.route('/metrics')
def metrics():
    all_files = db.fetch_files_from_repo('github-168152007')#TODO: get the repository name from the view
    all_commits = db.fetch_commits_from_repo('github-168152007')
    converted_graph = graph_drawer.draw_file_size(all_files)
    converted_pie = graph_drawer.draw_commit_authors(all_commits)
    converted_histogram = graph_drawer.draw_commit_history(all_commits)
    return render_template("metrics.html",bar_graph=converted_graph,pie_chart=converted_pie,histogram=converted_histogram)
