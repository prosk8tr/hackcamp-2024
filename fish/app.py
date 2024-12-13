import models
from flask import Flask, render_template, redirect, request, url_for
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

db = models.DbConnect()
repos = db.fetch_all_repositories()
graph_drawer = models.GraphDrawer()
global repo_id
repo_id=""

repo_compare = ["", ""]

@app.route('/')
def root():
    return redirect("/home")

@app.route('/home')
def home():
    return render_template("index.html")
    
@app.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method=='POST':
        #repo_id=request.form['rep']
        search_term = request.form.get('search-term')
        if search_term != "":
            search_results = repos.query('name.str.contains(@search_term, case=False) or owner.str.contains(@search_term, case=False)')
            return render_template("projects.html",repos=search_results)
        else: 
            return render_template("projects.html", repos=repos)
    else:
        return render_template("projects.html", repos=repos)


@app.route('/comparison', methods=['POST','GET'])
def comparison():
    selected_project_1 = request.form.get('project_1', '')
    selected_project_2 = request.form.get('project_2', '')

    if request.method=='POST':
        project_1=request.form['project_1']
        project_2=request.form['project_2']

        all_files_1 = db.fetch_files_from_repo(project_1)
        all_files_2 = db.fetch_files_from_repo(project_2)
        all_commits_1 = db.fetch_commits_from_repo(project_1)
        all_commits_2 = db.fetch_commits_from_repo(project_2)


        bar_compare = graph_drawer.compare_file_sizes(all_files_1,all_files_2)
        pie_charts = graph_drawer.compare_commit_authors(all_commits_1,all_commits_2)
        histograms = graph_drawer.compare_commit_history(all_commits_1,all_commits_2)

        project_1_title=repos.loc[repos['id']==project_1]
        project_1_title=project_1_title.values[0][1]
        project_2_title=repos.loc[repos['id']==project_2]
        project_2_title=project_2_title.values[0][1]
        
        return render_template("comparison.html",project_1_title=project_1_title,project_2_title=project_2_title,repos=repos,bar_graph=bar_compare,pie_chart_1=pie_charts[0],histogram_1=histograms[0],pie_chart_2=pie_charts[1],histogram_2=histograms[1],selected_project_1=selected_project_1, selected_project_2=selected_project_2)
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
    repo_data=repo_data.values[0]
    return render_template("metrics.html",bar_graph=converted_graph.to_html(),pie_chart=converted_pie.to_html(),histogram=converted_histogram.to_html(),repo_data=repo_data)

