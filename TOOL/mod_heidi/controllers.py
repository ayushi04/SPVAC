from flask import request, render_template, Blueprint, json, redirect, url_for, flash
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user
import random
import os
import pandas as pd
import config
import _pickle as cPickle

from mod_datacleaning import data_cleaning
from mod_heidi import heidi_results


mod_heidi_controllers = Blueprint('heidi_controllers', __name__)

@mod_heidi_controllers.route('/heidi')
def heidi():
    title=request.args.get('title')
    #user = request.args.get('user')
    #paramObj = jsonrequest.data.get('paramObj').to_dict()
    #print(paramObj['datasetPath'],'heidi_controllers')
    #return render_template('dimension_new.html', paramObj = paramObj) #title='dimension Visualization',datasetPath=datasetPath,user=current_user, dimensions=['a','b','c'])
