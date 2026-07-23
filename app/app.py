import os, re
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import CSRFProtect
import pymysql


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["FLASK_SECRET_KEY"]
csrf = CSRFProtect(app)

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
    # Binds to all interfaces intentionally: containerized app behind
    # nginx reverse proxy; exposure controlled by compose port mapping.
    app.run(host=os.environ.get("BIND_HOST", "0.0.0.0"), port=5000)