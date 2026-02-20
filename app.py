from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "database.db"

def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE presentations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                classe TEXT NOT NULL,
                enseignant TEXT NOT NULL,
                specialite TEXT NOT NULL,
                date_presentation TEXT NOT NULL,
                pendant_cours TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM presentations ORDER BY date_presentation DESC")
    data = cur.fetchall()
    conn.close()
    return render_template("index.html", data=data)

@app.route("/ajouter", methods=["GET", "POST"])
def ajouter():
    classes = ["2A", "2B", "2C"]
    specialites = ["NSI", "Maths", "Physique", "SVT"]
    enseignants = ["Alice", "Bob", "Charlie"]

    if request.method == "POST":
        classe = request.form["classe"]
        enseignant = request.form["enseignant"]
        specialite = request.form["specialite"]
        date = request.form["date"]
        pendant_cours = request.form["pendant_cours"]

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO presentations (classe, enseignant, specialite, date_presentation, pendant_cours)
            VALUES (?, ?, ?, ?, ?)
        """, (classe, enseignant, specialite, date, pendant_cours))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("formulaire.html", classes=classes, specialites=specialites, enseignants=enseignants)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))