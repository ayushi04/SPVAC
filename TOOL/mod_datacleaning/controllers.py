from flask import request, render_template, Blueprint, json, redirect, url_for, flash
from app import db, login_manager
#from mod_auth.models import User
from models import Dataset
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user
import random
import os
import pandas as pd
import config
import _pickle as cPickle

from mod_datacleaning import data_cleaning
from mod_heidi import heidi_results
from mod_heidi.controllers import mod_heidi_controllers
import json

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

mod_datacleaning_controllers = Blueprint('datacleaning_controllers', __name__)


@mod_datacleaning_controllers.route('/upload', methods=['POST'])
def upload():
    #try:
        file = request.files['file']
        filename = file.filename
        if filename=='':
            raise ValueError('No file uploaded!!')
        file_uploads_path = os.path.join(config.UPLOADS_DIR, filename)
        file_static_path = os.path.join(config.STATIC_DIR, 'output')
        file_static_path = os.path.join(file_static_path, filename)
        file.save(file_uploads_path)
        cleaned_file = ''
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

        #X =  Dataset.query.filter_by(name = filename)
        #for i in X:
        #    print(cPickle.loads(i.content))
        
        
        #SAVING INPUT DATASET TO DATABASE
        try:

            serialized_content = cPickle.dumps(cleaned_file) 
            #dataset = Dataset(filename, download_path, serialized_content)
            #db.session.add(dataset)
            #db.session.commit()
        except Exception as e:
            
            print(e)
            #raise ValueError('Dataset with this name already exist in database!. Please update dataset name')   
        
        del cleaned_file['classLabel']
        cleaned_file.index = cleaned_file['id']
        del cleaned_file['id']
        paramObj = heidi_results.getAllSubspaces(cleaned_file, filename)
        #return render_template('success.html', download_path=download_path, user=current_user)
        return render_template('dimension_new.html', title = 'visual tool', user = current_user, paramObj = paramObj) #title='dimension Visualization',datasetPath=datasetPath,user=current_user, dimensions=['a','b','c'])
        #return redirect(url_for('heidi_controllers.heidi', title='visual tool', user = current_user, paramObj = paramObj))
        #render_template('first.html',title='visual tool',datasetPath=download_path, user=current_user)
    #except Exception as e:
    #    print(e)
    #    PrintException()
    #    flash(PrintException())
    #    return render_template('index.html', user=current_user)
