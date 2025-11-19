import sqlite3
from flask import Flask, g
app = Flask(__name__)

class database:
    def __init__(self, app):
        self.app = app
        self.databaseName = 'timepal.db'
        self.databaseSql = "tp_database.sql"

    def getAll(self, tableName):
        with app.app_context():
            cur = self._get_db().cursor()
            rows = cur.execute(f"SELECT * FROM {tableName}").fetchall()
            cur.close()
            return rows

    def init_db(self):
        with app.app_context():
            db = self._get_db()
            with open(self.databaseSql, mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()

    def _get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(self.databaseName)
            db.row_factory = sqlite3.Row  # Allows accessing columns by name
        return db

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()
