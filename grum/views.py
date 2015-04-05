from grum import app, db
from grum.models import User
from flask import render_template, request, redirect
from flask.ext.login import login_user, login_required


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        # Login verification code
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first_or_404()
        if user.validate_password(password):
            login_user(user)
            return redirect("/mail")

    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm']

        if password != confirm_password:
            return redirect("/register")

        new_user = User(
            username=username,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(user)
        return redirect("/mail")
    
    return render_template("register.html")

@app.route("/mail")
@login_required
def mail():
    return render_template('mail.html')
