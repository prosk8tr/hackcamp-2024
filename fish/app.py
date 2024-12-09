import models
from flask import Flask, render_template, redirect, request, url_for
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

db = models.DbConnect()
repos = db.fetch_all_repositories()
graph_drawer = models.GraphDrawer()
repo_id=""

repo_compare = ["", ""]

@app.route('/')
def root():
    return redirect("/home")

@app.route('/home')
def home():
    return render_template("index.html")
    
@app.route('/page1', methods=['GET', 'POST'])
def page1():
    if request.method=='POST':
        repo_id=request.form['rep']
        print(repo_id)
    return render_template("page1.html", repos=repos)


@app.route('/comparison', methods=['POST','GET'])
def comparison():
    if request.method=='POST':
        project_1=request.form['project_1']
        project_2=request.form['project_2']

        all_files_1 = db.fetch_files_from_repo(project_1)
        all_commits_1 = db.fetch_commits_from_repo(project_1)
        all_files_2 = db.fetch_files_from_repo(project_2)
        all_commits_2 = db.fetch_commits_from_repo(project_2)


        bar_1 = graph_drawer.draw_file_size(all_files_1)
        pie_1 = graph_drawer.draw_commit_authors(all_commits_1)
        histogram_1 = graph_drawer.draw_commit_history(all_commits_1)
        bar_2 = graph_drawer.draw_file_size(all_files_2)
        pie_2 = graph_drawer.draw_commit_authors(all_commits_2)
        histogram_2 = graph_drawer.draw_commit_history(all_commits_2)

        project_1_title=repos.loc[repos['id']==project_1]
        project_1_title=project_1_title.values[0][1]
        project_2_title=repos.loc[repos['id']==project_2]
        project_2_title=project_2_title.values[0][1]
        
        return render_template("comparison.html",project_1_title=project_1_title,project_2_title=project_2_title,repos=repos,bar_graph_1=bar_1,pie_chart_1=pie_1,histogram_1=histogram_1,bar_graph_2=bar_2,pie_chart_2=pie_2,histogram_2=histogram_2)
    else:
        return render_template("comparison.html",repos=repos)

@app.route('/metrics', methods=['GET','POST'])
def metrics():
    repo_id=request.form['rep']
    all_files = db.fetch_files_from_repo(repo_id)
    all_commits = db.fetch_commits_from_repo(repo_id)
    converted_graph = graph_drawer.draw_file_size(all_files)
    converted_pie = graph_drawer.draw_commit_authors(all_commits)
    converted_histogram = graph_drawer.draw_commit_history(all_commits)
    repo_data=repos.loc[repos['id']==repo_id]
    print(repo_data.values[0][1])
    repo_data=repo_data.values[0]
    return render_template("metrics.html",bar_graph=converted_graph,pie_chart=converted_pie,histogram=converted_histogram,repo_data=repo_data)

