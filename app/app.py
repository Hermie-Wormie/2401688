import os, re
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# C3: allowlist — letters, digits, spaces, basic punctuation; 3–50 chars
PATTERN = re.compile(r"^[A-Za-z0-9 .,'-]{3,50}$")

def db():
    return pymysql.connect(
        host=os.environ["DB_HOST"], user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"], database=os.environ["DB_NAME"])

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/search", methods=["POST"])
def search():
    term = request.form.get("term", "").strip()
    if not PATTERN.fullmatch(term):          # attack or invalid -> back to home, input cleared
        return redirect(url_for("home"))
    with db() as conn, conn.cursor() as cur: # parameterized insert (no SQLi)
        cur.execute("INSERT INTO `2401688` (query, query_time) VALUES (%s, %s)",
                    (term, datetime.now()))
        conn.commit()
    return render_template("result.html", term=term)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)