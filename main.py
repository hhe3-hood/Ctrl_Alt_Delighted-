import sqlite3
from flask import Flask, render_template, g

app = Flask(__name__)
DATABASE = 'timepal.db'


@app.route("/")
def home():
    return render_template("login.html")


def init_db():
    with app.app_context():
        conn = sqlite3.connect(DATABASE)
        with open('tp_database.sql', mode='r') as f:
            conn.cursor().executescript(f.read())
        conn.commit()

# Run this once to create the database and tables

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Allows accessing columns by name
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    init_db()

    app.run()

