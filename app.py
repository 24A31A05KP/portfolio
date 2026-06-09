from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session
)

from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

import os
import config

app = Flask(__name__)
UPLOAD_FOLDER = "static/resume"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB
app.config['MYSQL_PORT'] = config.MYSQL_PORT
app.secret_key = config.SECRET_KEY

mysql = MySQL(app)


# ================= HOME =================
@app.route("/")
def home():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM projects")
    projects = cur.fetchall()
    
    cur.close()

    return render_template(
        "index.html",
        projects=projects
    )


# ================= CONTACT =================
@app.route("/contact", methods=["POST"])
def contact():

    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO contacts(name, email, message)
        VALUES (%s, %s, %s)
    """, (name, email, message))

    mysql.connection.commit()
    cur.close()

    return redirect("/")


# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT * FROM admin
            WHERE username=%s
            AND password=%s
        """, (username, password))

        user = cur.fetchone()

        if user:
            session["admin"] = username
            return redirect("/admin")

    return render_template("login.html")


# ================= ADMIN =================
@app.route("/admin")
def admin():

    if "admin" not in session:
        return redirect("/login")

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM projects")
    projects = cur.fetchall()
    project_count = len(projects)
    edit_id = request.args.get("edit")

    edit_project = None

    if edit_id:
        cur.execute(
            "SELECT * FROM projects WHERE id=%s",
            (edit_id,)
        )

    edit_project = cur.fetchone()

    cur.execute("SELECT * FROM contacts")
    messages = cur.fetchall()
    message_count = len(messages)
    return render_template(
    "admin.html",
    projects=projects,
    messages=messages,
    edit_project=edit_project,
    project_count=project_count,
    message_count=message_count
        )


# ================= ADD PROJECT =================
@app.route("/add-project", methods=["POST"])
def add_project():

    if "admin" not in session:
        return redirect("/login")

    title = request.form["title"]
    description = request.form["description"]
    tech_stack = request.form["tech_stack"]
    github = request.form["github"]
    live = request.form["live"]

    cur = mysql.connection.cursor()

    # Check duplicate
    cur.execute(
        "SELECT * FROM projects WHERE title=%s",
        (title,)
    )

    existing_project = cur.fetchone()

    if existing_project:
        return redirect("/admin")

    cur.execute("""
        INSERT INTO projects
        (
            title,
            description,
            tech_stack,
            github_link,
            live_link
        )

        VALUES (%s, %s, %s, %s, %s)
    """, (
        title,
        description,
        tech_stack,
        github,
        live
    ))

    mysql.connection.commit()

    return redirect("/admin")


# ================= DELETE PROJECT =================
@app.route("/delete-project/<int:id>")
def delete_project(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM projects WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    return redirect("/admin")

# ================= UPDATE PROJECT =================
@app.route("/update-project/<int:id>", methods=["POST"])
def update_project(id):

    if "admin" not in session:
        return redirect("/login")

    title = request.form["title"]
    description = request.form["description"]
    tech_stack = request.form["tech_stack"]
    github = request.form["github"]
    live = request.form["live"]

    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE projects
        SET
        title=%s,
        description=%s,
        tech_stack=%s,
        github_link=%s,
        live_link=%s
        WHERE id=%s
    """, (
        title,
        description,
        tech_stack,
        github,
        live,
        id
    ))

    mysql.connection.commit()

    return redirect("/admin")
# ================= DELETE MESSAGE =================
@app.route("/delete-message/<int:id>")
def delete_message(id):

    if "admin" not in session:
        return redirect("/login")

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    return redirect("/admin")    
# ================= LOGOUT =================
@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect("/")

# ================= UPLOAD RESUME =================
@app.route("/upload-resume", methods=["POST"])
def upload_resume():

    if "admin" not in session:
        return redirect("/login")

    file = request.files["resume"]

    if file:

        filename = secure_filename("resume.pdf")

        file.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )
        )

    return redirect("/admin")
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )