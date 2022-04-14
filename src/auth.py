from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in", category='success')
                login_user(user, remember=True)
                return redirect(url_for('pages.dashboard'))
            else:
                flash("Incorrect email or password", category='error')
        else:
            flash("Incorrect email or password", category='error')

    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        name = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # checks whether a user has already signed up and checks whether their email is stored in the User database
        email_exists = User.query.filter_by(email=email).first()
        name_exits = User.query.filter_by(name=name).first()
        if email_exists:
            flash('An account with this email already exists', category='error')
        elif name_exits:
            flash('An account with this name already exists', category='error')
        elif password1 != password2:
            flash('Password does not match', category='error')
        elif len(password1) < 8:
            flash('Password is too short', category='error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('User created!')
            return redirect(url_for('auth.login'))

    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
