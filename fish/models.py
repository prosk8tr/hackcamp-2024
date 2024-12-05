import os
import psycopg

class db_connect:
    #Class variables are shared between every instance of a class.
    url = os.getenv("DATABASE_URL") #Get the URL of the database in the .env config
    connection = psycopg.connect(url) #Open connection to the database
    cursor = connection.cursor() #This is what allows select queries

    def get_repos(self):
        SQL = """SELECT * FROM repositories;"""
        self.cursor.execute(SQL)
        repos = self.cursor.fetchall()
        results = []
        for repo in repos:
            results.append(repo)
        return results


class repository:
    