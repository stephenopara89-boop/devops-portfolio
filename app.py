from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text, nullable=False)

    technologies = db.Column(db.String(200), nullable=False)

    github_url = db.Column(db.String(200))

    live_url = db.Column(db.String(200))


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/about")
def about():

    return render_template("about.html")


@app.route("/projects")
def projects():

    projects = Project.query.all()

    return render_template(
        "projects.html",
        projects=projects
    )


@app.route("/projects/add", methods=["GET", "POST"])
def add_project():

    if request.method == "POST":

        project = Project(
            name=request.form["name"],
            description=request.form["description"],
            technologies=request.form["technologies"],
            github_url=request.form.get("github_url", ""),
            live_url=request.form.get("live_url", "")
        )

        db.session.add(project)

        db.session.commit()

        return redirect(url_for("projects"))

    return render_template("add_project.html")


@app.route("/projects/edit/<int:project_id>", methods=["GET", "POST"])
def edit_project(project_id):

    project = Project.query.get_or_404(project_id)

    if request.method == "POST":

        project.name = request.form["name"]

        project.description = request.form["description"]

        project.technologies = request.form["technologies"]

        project.github_url = request.form.get("github_url", "")

        project.live_url = request.form.get("live_url", "")

        db.session.commit()

        return redirect(url_for("projects"))

    return render_template(
        "edit_project.html",
        project=project
    )


@app.route("/projects/delete/<int:project_id>", methods=["POST"])
def delete_project(project_id):

    project = Project.query.get_or_404(project_id)

    db.session.delete(project)

    db.session.commit()

    return redirect(url_for("projects"))


@app.route("/contact")
def contact():

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
