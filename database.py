import sqlite3
from flask import Flask, g

app = Flask(__name__)
DATABASE = 'database.db'



class dbTable:
    def __init__(self, tableName):
        self.tableName = ""
        self.databaseLocation = "project_database.sql"
        self.hasTable = False

    def getTable(self):
        tbl = getattr(g, self.tableName, None)
        if tbl is None:
            tbl = g._database = sqlite3.connect(self.tableName)
            tbl.row_factory = sqlite3.Row
        return tbl

