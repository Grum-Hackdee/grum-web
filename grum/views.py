from grum import app, db
from grum.models import User
from flask import render_template, request, redirect


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        # Login verification code
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first_or_404()
        if user.validate_password(password):
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

        return redirect("/mail")
    
    return render_template("register.html")

@app.route("/mail")
def mail():
    return render_template('mail.html')
