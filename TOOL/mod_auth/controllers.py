from flask import request, render_template, Blueprint, json, redirect, url_for, flash
from app import db, login_manager
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user
import random
import os
import pandas as pd
import config
from mod_datacleaning import data_cleaning

mod_controllers = Blueprint('controllers', __name__)

@mod_controllers.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            user = User(request.form['name'], request.form['phone'], generate_password_hash(
                request.form['password'], method='sha256'), request.form['email'])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('controllers.login'))
        except Exception as e:
            print(e)
            flash('Wrong inputs, please check your input and try again.')
            return render_template('register.html', user=current_user)
    else:
        return render_template('register.html', user=current_user)


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None


@mod_controllers.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        if not current_user.is_anonymous:
            return render_template('index.html', user=current_user)
        return render_template('login.html', user=current_user)
    else:
        user = User.query.filter(User.email == request.form['email']).first()
        if user:
            if check_password_hash(user.password, request.form['password']):
                login_user(user)
                return render_template('index.html', user=current_user)
            else:
                flash('Wrong password.')
                return render_template('login.html', user=current_user)
        else:
            flash('Username doesn\'t exist.')
            return render_template('login.html', user=current_user)


@mod_controllers.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('controllers.index'))


@mod_controllers.route('/', methods=['GET'])
def index():
    return render_template('index.html', user=current_user)

@mod_controllers.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html', user=current_user)


@login_required
@mod_controllers.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'GET':
        colors = ['primary', 'success', 'info', 'warning', 'danger']
        return render_template('account.html', user=current_user, color=random.choice(colors))
    else:
        try:
            if check_password_hash(current_user.password, request.form['oldpassword']):
                current_user.password = generate_password_hash(
                    request.form['newpassword'], method='sha256')
                db.session.commit()
                return redirect(url_for('controllers.index'))
            else:
                flash('Enter current password correctly and try again.')
                return redirect(url_for('controllers.account'))
        except:
            flash('Some error occurred, please try again later.')
            return redirect(url_for('controllers.account'))
