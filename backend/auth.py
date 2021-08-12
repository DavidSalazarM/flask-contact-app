from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import Users
from flask_login import login_user, logout_user, login_required
from __init__ import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = Users.query.filter_by(email=email).first()
        if not user:
            flash('Please sign up before!')
            return redirect(url_for('auth.login'))
        elif not check_password_hash(user.password, password):
            flash('Please check your password and try again.')
            return redirect(url_for('auth.login'))
        login_user(user, remember=remember)
        return redirect(url_for('main.index'))
    else:
        return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).first() 
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        new_user = Users(email=email, name=name, \
                        password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
