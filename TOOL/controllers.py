from flask import request, session, render_template, Blueprint, json, redirect, url_for, flash
from app import db, login_manager
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user
import random
import os
import pandas as pd
import config
from mod_datacleaning import data_cleaning
    
import linecache
import sys
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    return ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

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


@mod_controllers.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        filename = file.filename
        if filename=='':
            raise ValueError('No file uploaded!!')
        file_uploads_path = os.path.join(config.UPLOADS_DIR, filename)
        file_static_path = os.path.join(config.STATIC_DIR, 'output')
        file_static_path = os.path.join(file_static_path, filename)
        file.save(file_uploads_path)
        if (filename.rsplit('.', 1)[1].lower() == 'csv'):
            dirty_file = pd.read_csv(file_uploads_path, sep=',')
            res = data_cleaning.id_classLabel_check(dirty_file)
            if(res!=True):
                raise ValueError(res)
            missing_val_fixed_file = data_cleaning.fix_missing(dirty_file, request.form['fix'])
            cleaned_file = data_cleaning.clean(missing_val_fixed_file)
            cleaned_file.to_csv(file_uploads_path, sep=',',index=False)
        elif (filename.rsplit('.', 1)[1].lower() == 'tsv'):
            dirty_file = pd.read_csv(file_uploads_path, sep='\t')
            missing_val_fixed_file = data_cleaning.fix_missing(
                dirty_file, request.form['fix'])
            cleaned_file = data_cleaning.clean(missing_val_fixed_file)
            cleaned_file.to_csv(file_uploads_path, sep=',',index=False)
        elif (filename.rsplit('.', 1)[1].lower() == 'json'):
            print (str(file_uploads_path))
            dirty_file = pd.read_json(str(file_uploads_path))
            missing_val_fixed_file = data_cleaning.fix_missing(
                dirty_file, request.form['fix'])
            cleaned_file = data_cleaning.clean(missing_val_fixed_file)
            cleaned_file.to_json(file_uploads_path)
        else:
            raise ValueError('Invalid file input! Please check the input file type')

        download_path = 'static/uploads/' + filename
        #return render_template('success.html', download_path=download_path, user=current_user)
        return render_template('first.html',title='visual tool',datasetPath=download_path, user=current_user)
    except Exception as e:
        print(e)
        PrintException()
        flash(PrintException())
        return render_template('index.html', user=current_user)

@mod_controllers.route('/contact', methods=['GET'])
def contact():
    print(current_user.name)
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
