import os
import psycopg
import pandas
import plotly
import plotly.express as px

class GraphDrawer:
    def draw_file_size(self,files): #draws a bar chart of the size of every file.
        # Create Bar chart
        fig = px.bar(files, x='name', y='line_count', color='name', barmode='group') #TODO: find a way to make the axis names look less python-y

        return fig.to_html() #return as html string, so it can be used in the view
        #TODO:switch between functional line count and all line count

class DbConnect:
    def __init__(self):
        #Class variables are shared between every instance of a class.
        self.url = os.getenv("DATABASE_URL") #Get the URL of the database in the .env config
        self.connection = psycopg.connect(self.url) #Open connection to the database
        self.cursor = self.connection.cursor() #This is what allows select queries

    def fetch_all_repositories(self):
        self.cursor.execute("SELECT id, name, owner, modified_at FROM repositories;")
        
        results=self.cursor.fetchall()

        columns = []
        for col in self.cursor.description: #gets the column names
            columns.append(col[0])

        all_repos = pandas.DataFrame(data=results,columns=columns) #makes a dataframe with the query results as data and column names
        all_repos['modified_at'] = pandas.to_datetime(all_repos['modified_at']).dt.strftime('%Y-%m-%d %H:%M:%S') #Change the format displayed for the modified_at data
        return all_repos
    

    def fetch_files_from_repo(self, repo_name):
        #Prepare the file path
        root_folder = repo_name + "%" #To search for any file path that starts with the repo name
        #Only get files i.e. those that are not directories
        SQL = "SELECT id, path, name, line_count, functional_line_count FROM files WHERE path LIKE (%s) AND is_directory='f';" 
        self.cursor.execute(SQL,(root_folder,))
        results = self.cursor.fetchall() #Do query

        columns = []
        for col in self.cursor.description:
            columns.append(col[0])
        all_files = pandas.DataFrame(data=results,columns=columns)
        return all_files

    def fetch_commits_from_repo(self, repo_id):
        SQL = "SELECT id, author, repository_id FROM commits where repository_id=(%s);"
        self.cursor.execute(SQL,(repo_id,))
        results = self.cursor.fetchall() #Do query

        columns = []
        for col in self.cursor.description:
            columns.append(col[0])
        all_commits = pandas.DataFrame(data=results,columns=columns)
        return all_commits
    
