from grum import app
from flask import render_template, request


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == "POST":
        username = request.form('username')
        password = request.form('password')
        confirm_password = request.form('confirm')
    
    return render_template("register.html")

@app.route("/mail")
def mail():
    return render_template('mail.html')
