
'''

Blog Model

Create a class to interface with sqlite3.  This type of object is typically called a "Model".

The table in sqlite3 will have two columns: post_name and post_text

Discuss with your neighbour on how to solve this challenge.

To connect Python to SQL, reference the following:
http://www.pythoncentral.io/introduction-to-sqlite-in-python/

Your model should be able to:

1) Open a sqlite3 db connection
2) Close the connection
3) Create a new table with the correct fields
4) Read by id where id is the primary key of the row
   this will return the blog data associated with that row in a string format
5) Insert a new blogpost - where you can add a new blog post and title

'''

import sqlite3


class BlogModel():
    def __init__(self,db_file):
        self.db_file = db_file
        self.post_name = None
        self.post_text = None
        self.conn = self.open()

    def open(self):
        "open sqlite3 db connection"
        return sqlite3.connect(self.db_file)

    def close(self):
        "close the connection to sqlite3"
        self.conn.close()

    def create_table(self):
        #create the table
        c = self.conn.cursor()
        c.execute("DROP TABLE IF EXISTS tab")
        c.execute("CREATE TABLE posts(id INTEGER PRIMARY KEY, post_name, post_text);")
        self.conn.commit()

    def insert(self, post_name, post_text):
        #create a new row with data that you pass in
        c = self.conn.cursor()
        c.execute("INSERT INTO posts(post_name, post_text) VALUES (\'%s\',\'%s\');" % (post_name, post_text))
        self.conn.commit()

    def read(self,id_):
        # "search for id, and return post_name and post_text as a string"
        c = self.conn.cursor()
        return c.execute("SELECT post_name, post_text FROM posts WHERE id=\'%s\'" % id_).fetchall()[0]

    def readall(self):
        c = self.conn.cursor()
        return c.execute("SELECT id, post_name, post_text FROM posts").fetchall()

    def latest_id(self):
        c = self.conn.cursor()
        return c.execute("SELECT MAX(id) FROM posts").fetchall()[0]


