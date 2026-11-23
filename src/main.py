from flask import Flask, request, render_template, g, jsonify
import sqlite3

DB = "data.db"
app = Flask(__name__)

def get_db():
  if "db" not in g:
    g.db = sqlite3.connect(DB)

    g.db.row_factory = sqlite3.Row

    g.db.execute("PRAGMA foreign_keys = ON")

  return g.db  

@app.teardown_appcontext            # Flask calls this automatically when a request finishes.
def close_db(exception):
  db = g.pop("db", None)          # take the connection out of `g` (or None if there wasn't one).
  if db is not None:
    db.close()   

def init_db():
  conn = sqlite3.connect(DB)

  conn.row_factory = sqlite3.Row

  curs = conn.cursor()

  curs.executescript("""

  CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    role TEXT,
    email TEXT, 
    password_hash TEXT UNIQUE
  );

  CREATE TABLE IF NOT EXISTS Cleaners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    points INTEGER,
    user_id INTEGER,
    FOREIGN KEY (user_id)
      REFERENCES Users(id)
  );

  CREATE TABLE IF NOT EXISTS Cleaning_History (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT,
    images TEXT,
    cleaner_id INTEGER,
    FOREIGN KEY (cleaner_id)
      REFERENCES Cleaners(id)
  );

  CREATE TABLE IF NOT EXISTS Reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review TEXT,
    given_points REAL,
    evaluator_id INTEGER NOT NULL,
    cleaning_session_id INTEGER NOT NULL,
    FOREIGN KEY (evaluator_id) REFERENCES Users(id),
    FOREIGN KEY (cleaning_session_id) REFERENCES Cleaning_History(id)
  );

  CREATE TABLE IF NOT EXISTS Weeks_History (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_number INTEGER,
    week_dictator TEXT,
    winning_points REAL
  );
  """)

  conn.commit()
  conn.close()

# Landing Page
@app.route("/")
def landing():
  return render_template("landing.html")

@app.route("/api/leader-board", methods=["GET"])
def get_leader_board():
  db = get_db()

  curs = db.cursor()

  rows = curs.execute("""
  SELECT c.points, u.name
  FROM Cleaners AS c
  LEFT JOIN Users AS u
  ON c.user_id = u.id
  ORDER BY points DESC
  """).fetchall()

  data = [dict(row) for row in rows]
  return jsonify(data)

@app.route("/api/week_dictator", methods=["GET"])
def get_last_week_dictator():
  db = get_db()

  curs = db.cursor()

  row = curs.execute("""
    SELECT week_dictator, winning_points FROM Weeks_History ORDER BY id DESC
  """).fetchone()

  if row is None:
    return jsonify([])

  data = [dict(row)]

  return jsonify(data)

if __name__ == "__main__":
  init_db()
  app.run()
  