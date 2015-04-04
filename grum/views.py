from grum import app
from flask import render_template


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template("register.html")
