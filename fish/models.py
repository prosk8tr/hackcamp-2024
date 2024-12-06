import os
import psycopg

class db_connect:
    def __init__(self):
        #Class variables are shared between every instance of a class.
        self.url = os.getenv("DATABASE_URL") #Get the URL of the database in the .env config
        self.connection = psycopg.connect(self.url) #Open connection to the database
        self.cursor = self.connection.cursor() #This is what allows select queries

    def get_all_repositories(self): #Used to get list of repositories for the view
        SQL = """SELECT id, name, owner FROM repositories;"""
        self.cursor.execute(SQL)
        results = self.cursor.fetchall() #Do query

        all_repositories = [] #Array of objects

        for result in results:
            row = [result[0],result[1],result[2]] #Make a list with the required values for the object attributes
            new_repo = repo(*row) #Make a repository object 
            print(new_repo.get_name()+new_repo.get_id()+new_repo.get_owner())
            all_repositories.append(new_repo)
        return all_repositories

        def get_files_from_repo(repo_name):
            pass

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
    def __init__(self, file_id, path, name, line_count, functional_line_count):
        self.file_id = file_id
        self.path = path
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
    
    def get_name(self):
        return self.name
    
    def get_author(self):
        return self.author
    
    def get_repository_id(self):
        return repository_id



