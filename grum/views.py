from grum import app
from flask import render_template


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():

    # check if post...
    username = request.form('username')
    password = request.form('password')
    confirm = request.form('confirm')
    
    return render_template("register.html")
