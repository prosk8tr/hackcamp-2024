import os
import psycopg
import pandas
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

class GraphDrawer:
    def draw_file_size(self,files): #draws a bar chart of the size of every file.
        #prepare the data; group into categories
        bins = pandas.cut(files['line_count'], [0,50,100,500,1000,np.inf])
        count = bins.value_counts() #returns the count of how many rows fit into each bin
        count=count.sort_index(ascending=True) #just makes sure the bars are sorted from lowest line count to highest
        count.index=['0-50','50-100','100-500','500-1000','1000+']
        file_size_data=pandas.DataFrame(count, columns=['count']) #new dataframe containing the data we just calculated ^
        file_size_data.index=file_size_data.index.astype(str)#so it can be turned into html string

        # Create Bar chart
        fig = px.bar(file_size_data, x=file_size_data.index, y='count',  barmode='group')
        fig.update_traces(marker_color="#CF7336", opacity=0.9, hovertemplate='Lines of code: %{x} <br>Files: %{y}') # decide the color of the bars in the chart, set hover label text

        #TODO: find a way to make the axis names look less python-y
        fig.update_layout(xaxis_title='Lines of Code', yaxis_title='Number of Files')
        fig.update_layout(
            {
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
                "plot_bgcolor": "rgba(0, 0, 0, 0)",
                "font_color":"white"
            }
        )

        return fig
        #TODO:switch between functional line count and all line count

    def draw_commit_authors(self,commits):
        fig = px.pie(commits, values='id', names='author', color_discrete_sequence=px.colors.sequential.Oranges_r) #the last attribute decides the color of the pie chart
        fig.update_traces(hovertemplate='Author: %{label} <br>Commits: %{value}')
        fig = px.pie(commits, values='id', names='author', color_discrete_sequence=px.colors.sequential.Oranges_r) #the last attribute decides the color of the pie chart
        fig.update_traces(hovertemplate='Author: %{label} <br>Commits: %{value}')
        fig.update_layout(
            {
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
                "plot_bgcolor": "rgba(0, 0, 0, 0)",
                "font_color":"white",
            }
        )
        return fig
    
    def compare_commit_authors(self,project_1_commits,project_2_commits):#Create both pie charts together so they render at the same time.
        fig1 = self.draw_commit_authors(project_1_commits)
        fig2 = px.pie(project_2_commits, values='id', names='author', color_discrete_sequence=px.colors.sequential.YlOrRd_r)
        fig2.update_traces(hovertemplate='Author: %{label} <br>Commits: %{value}')
        fig2.update_layout(
            {
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
                "plot_bgcolor": "rgba(0, 0, 0, 0)",
                "font_color":"white",
            }
        )
        
        return [fig1.to_html(),fig2.to_html()] #Return both pie charts in a list so they can be used seperately
    
    def compare_commit_history(self,project_1_commits,project_2_commits):
        fig1 = self.draw_commit_history(project_1_commits)
        fig2 = self.draw_commit_history(project_2_commits)
        fig2.update_traces(marker_color="#bc0128")

        return [fig1.to_html(),fig2.to_html()]

    def compare_file_sizes(self,project_1_files,project_2_files):
        # Create bar charts
        fig1 = self.draw_file_size(project_1_files)
        fig2 = self.draw_file_size(project_2_files)
        fig2.update_traces(marker_color="#bc0128")
        fig2.update_traces(marker_color="#bc0128")

        #combine the graphs
        fig_combined = go.Figure()
        fig_combined.add_trace(go.Bar(
            x=fig1.data[0].x, 
            y=fig1.data[0].y, 
            name='Project 1', 
            marker_color="#CF7336",
            opacity=0.9,
            hovertemplate='Lines of code: %{x} <br>Files: %{y}'
        ))
        fig_combined.add_trace(go.Bar(
            x=fig2.data[0].x, 
            y=fig2.data[0].y, 
            name='Project 2', 
            marker_color="#bc0128",
            opacity=0.9,
            hovertemplate='Lines of code: %{x} <br>Files: %{y}'
        ))
        fig_combined.update_layout(xaxis_title='Lines of Code', yaxis_title='Number of Files')
        fig_combined.update_layout(
            {
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
                "plot_bgcolor": "rgba(0, 0, 0, 0)",
                "font_color":"white",
            }
        )

        return fig_combined.to_html() #return as html string, so it can be used in the view
        #TODO:switch between functional line count and all line count
        

    def draw_commit_history(self,commits):
        fig = px.histogram(commits, x="date")
        fig.update_traces(xbins_size="M1")
        fig.update_traces(marker_color="#CF7336",opacity=0.9, hovertemplate='Date: %{x} <br>Commits: %{y}') # decide the color of the blocks of data in the graph
        fig.update_layout(xaxis_title='Time', yaxis_title='Number of commits')
        fig.update_traces(marker_color="#CF7336",opacity=0.9, hovertemplate='Date: %{x} <br>Commits: %{y}') # decide the color of the blocks of data in the graph
        fig.update_layout(xaxis_title='Time', yaxis_title='Number of commits')
        fig.update_layout(
            {
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
                "plot_bgcolor": "rgba(0, 0, 0, 0)",
                "font_color":"white",
            }
        )
        #Add histogram drop down to choose how precise the histogram is:
        fig.update_layout(xaxis_rangeslider_visible=True,
                          updatemenus=[
                              dict(
                                active = 3,
                                bgcolor = "#212429",
                                bordercolor = "#212429",
                              buttons = [
        dict(
            args = ['xbins.size', ' 3600000.0'],
            label = 'Hour',
            method = 'restyle',
        ), dict(
            args = ['xbins.size', '86400000.0'],
            label = 'Day',
            method = 'restyle',
        ), dict(
            args = ['xbins.size', ' 604800000.0'],
            label = 'Week',
            method = 'restyle',
        ), dict(
            args = ['xbins.size', 'M1'],
            label = 'Month',
            method = 'restyle',
        )]
                          )])

class DbConnect:
    def __init__(self):
        #Class variables are shared between every instance of a class.
        self.url = os.getenv("DATABASE_URL") #Get the URL of the database in the .env config
        self.connection = psycopg.connect(self.url) #Open connection to the database
        self.cursor = self.connection.cursor() #This is what allows select queries

    def fetch_all_repositories(self):

        self.cursor.execute("""SELECT id, name, owner, modified_at,
        (SELECT COUNT(commits.id) AS commit_count FROM commits WHERE repositories.id=commits.repository_id),
        (SELECT COUNT(DISTINCT author) AS contributor_count FROM commits WHERE repositories.id=commits.repository_id),
        (SELECT COUNT(files.id) AS file_count FROM files WHERE is_directory='f'
        AND files.branch_id=(SELECT id FROM branches where branches.repository_id=repositories.id))
        FROM repositories;""")
        results=self.cursor.fetchall()

        columns = []
        for col in self.cursor.description: #gets the column names
            columns.append(col[0])

        all_repos = pandas.DataFrame(data=results,columns=columns) #makes a dataframe with the query results as data and column names
        all_repos['modified_at'] = pandas.to_datetime(all_repos['modified_at']).dt.strftime('%Y-%m-%d %H:%M:%S') #Change the format displayed for the modified_at data
        return all_repos


    def fetch_files_from_repo(self, repo_id):
        #Prepare the file path#
        SQL = "SELECT id, path, name, line_count, functional_line_count FROM files WHERE branch_id=(SELECT id FROM branches WHERE branches.repository_id=(%s)) AND is_directory='f';"
        self.cursor.execute(SQL,(repo_id,))
        results = self.cursor.fetchall() #Do query

        columns = []
        for col in self.cursor.description:
            columns.append(col[0])
        all_files = pandas.DataFrame(data=results,columns=columns)
        return all_files

    def fetch_commits_from_repo(self, repo_id):
        SQL = "SELECT id, author, date, repository_id FROM commits where repository_id=(%s);"
        self.cursor.execute(SQL,(repo_id,))
        results = self.cursor.fetchall() #Do query

        columns = []
        for col in self.cursor.description:
            columns.append(col[0])
        all_commits = pandas.DataFrame(data=results,columns=columns)
        return all_commits
