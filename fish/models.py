import os
import psycopg

class db_connect:
    def __init__(self):
        #Class variables are shared between every instance of a class.
        self.url = os.getenv("DATABASE_URL") #Get the URL of the database in the .env config
        self.connection = psycopg.connect(self.url) #Open connection to the database
        self.cursor = self.connection.cursor() #This is what allows select queries

    def fetch_all_repositories(self): #Used to get list of repositories for the view
        SQL = """SELECT id, name, owner FROM repositories;"""
        self.cursor.execute(SQL)
        results = self.cursor.fetchall() #Do query

        all_repositories = [] #Array of repositories

        for result in results:
            row = [result[0],result[1],result[2]] #Make a list with the required values for the object attributes
            new_repo = repo(*row) #Make a repository object
            all_repositories.append(new_repo)
        return all_repositories

    def get_commits_from_repo(self, repo_name):
        pass
        #TODO everything
        
    def get_files_from_repo(self, repo_name):
        pass #Add later
        #Prepare the file path
        #root_folder = repo_name + "%" #To search for any file path that starts with the repo name
        #Only get files i.e. those that are not directories
        #TODO change to REGEXP_LIKE?
        #SQL = "SELECT id, path, name, line_count, functional_line_count FROM files WHERE path LIKE (%s) AND is_directory='f';" 



class repo:
    def __init__(self, repo_id, name, owner):
        self.repo_id = repo_id
        self.name = name
        self.owner = owner
    
    def get_id(self):
        return self.repo_id
    
    def get_name(self):
        return self.name

    def get_owner(self):
        return self.owner

class repo_file:
    def __init__(self, file_id, name, line_count, functional_line_count):
        self.file_id = file_id
        self.name = name
        self.line_count = line_count
        self.functional_line_count = functional_line_count
    
    def get_id(self):
        return self.file_id

    def get_path(self):
        return self.path

    def get_name(self):
        return self.name

    def get_line_count(self):
        return self.line_count

    def get_functional_line_count(self):
        return self.functional_line_count

class commit:
    def __init__(self, commit_id, name, author, repository_id):
        self.commit_id = commit_id
        self.name = name
        self.author = author
        self.repository_id = repository_id
    
    def get_commit_id(self):
        return self.commit_id
    
    def get_author(self):
        return self.author
    
    def get_repository_id(self):
        return self.repository_id



