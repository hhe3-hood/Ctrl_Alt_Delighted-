import sqlite3
from flask import Flask, render_template

from dbLib import database

app = Flask(__name__)
DATABASE = 'timepal.db'


@app.route("/")
def home():
    return render_template("login.html")

if __name__ == "__main__":

    dbCnn = database(app)
    dbCnn.init_db()
    testRows = dbCnn.getAll("Color_Schemes")
    for row in testRows:
        print(row["name"], row["primary_color"])

    app.run()

