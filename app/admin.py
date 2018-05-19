from app import app
from flask import render_template

@app.route("/")
def student():
    return render_template("student.html")

@app.route('/lecturer')
def lecturer():
    return render_template('lecturer.html')