from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Créer la base de données si elle n'existe pas
if not os.path.exists("tasks.db"):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT)")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route('/add', methods=["POST"])
def add():
    title = request.form["title"]
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
