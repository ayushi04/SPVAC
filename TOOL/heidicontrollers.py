import random
#import matlab.engine
import os
import pandas as pd
import config
import time
import math
import json
import ast
from flask import request, render_template, Blueprint, json, redirect, url_for, flash
from app import db, login_manager
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user
import matplotlib.pyplot as plt
from models import ImageDB,Legend,TopLegend,ImageInfo
import numpy as np

#from bokeh.plotting import figure, output_file, show
#from bokeh.embed import components
#from bokeh.resources import CDN
#from bokeh.embed import file_html
from PIL import ImageChops

#import heidicontroller_helper as hch
from mod_dim import best_heidi_img as hd
from mod_dim import heidiHelper as hh
from mod_dim import orderPoints as op
#from mod_dim import compressed_heidi as ch
from mod_dim import bea2
from mod_dim import region_label as rg
from mod_dim import database_connectivity_rdb as dbc

#eng = matlab.engine.start_matlab()

mod_heidicontrollers = Blueprint('heidicontrollers', __name__)

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


@mod_heidicontrollers.route('/heidi')
def heidi():
    datasetPath=request.args.get('datasetPath')
    return render_template('dimension.html',title='dimension Visualization',datasetPath=datasetPath,user=current_user)

# THIS METHOD IS MAIN METHOD WHICH IS USED TO CREATE HEIDI IMAGE
@mod_heidicontrollers.route('/image')
def image():
    #print('---heidicontrollers:image()------')

    #---------------1. INPUT PARAMETER READING ----------------------------------------------
    #INPUT PARAMS FROM WEB PAGE (DIMENSION.HTML)
    #try:    
        order_dim = request.args.get('order_dim')
        selected_dim = request.args.get('selectedDim')
        datasetPath = request.args.get('datasetPath')
        grid = request.args.get('grid')
        knn = int(request.args.get('knn'))
        imgType='_'+request.args.get('imgType')
        if(grid=='yes'): grid=True
        else: grid=False
        rowfilterDict = ast.literal_eval(request.args.get('filterDict'))
        print('params',order_dim,selected_dim,datasetPath,rowfilterDict,imgType,knn)
        
        # write code here for error handling if order_dim is invalid

        # READING THE DATASET
        data=pd.read_csv(filepath_or_buffer=datasetPath,sep=',',index_col='id')
        

        #IF THERE IS ANY ROW FILTER OPTION, FILTERING OF ROWS
        for k in rowfilterDict.keys():
            data=data.loc[data[k].isin([rowfilterDict[k]])]

        #CONVERT JAVASCRIPT OBJECT OF ORDERDIM IN PYTHON LIST
        dim=[]
        if (order_dim!=''):
            dim=[s for s in order_dim.split(' ')]

        #FILTERING THE COLUMNS IN ORDERDIM AND CLASSLABEL
        filtered_data=pd.concat([data.loc[:,dim+['classLabel']],data.loc[:,list(rowfilterDict.keys())]],axis=1)
        #filename_data=hd.normalize_data(filtered_data)
        filtered_data['classLabel_orig']=filtered_data['classLabel'].values
        #filtered_data=filtered_data.drop(list(rowfilterDict.keys()),axis=1)
        print(filtered_data.columns,filtered_data)

        #---------------2. ORDERING POINTS ----------------------------------------------

        # IF ORDERDIM LENGTH =1 THEN ORDERING BY SORTED ORDER ELSE SOME OTHER ORDERING SCHEMA
        if len(dim)==1:
            param={}
            param['columns']=list(filtered_data.columns[:-1])
            param['order']=[True for i in param['columns']]
            sorted_data=op.sortbasedOnclassLabel(filtered_data,'dimension',param)
            # REINDEXING THE INPUT DATA (TO BE USED LATER)
            sorting_order=sorted_data.index
            data=data.reindex(sorting_order)
        else:
            print('mst ordering')
            param={}
            sorted_data=op.sortbasedOnclassLabel(filtered_data,'knn_bfs',param)#'mst_distance' #connected_distance
            #sorted_data=op.sortbasedOnclassLabel(filtered_data,'euclidian_distance',param)
            sorting_order=sorted_data.index
            data=data.reindex(sorting_order)

            '''4-JUNE BEA (UNCOMMENT IF YOU WANT BEA)
            output='static/output'
            t=filtered_data.copy()
            del t['classLabel_orig']
            hd_matrix,_,_=hd.generateHeidiMatrixResults_noorder(output,t,20) # remove waste sorted_data
            #print(hd_matrix)
            c=filtered_data['classLabel'].values
            print('calling bea')
            sorting_order=bea2.BEA_clusterwise(hd_matrix,c)
            #print('sorted order obtained is ',sorting_order)
            filtered_data['classLabel_orig']=filtered_data['classLabel']
            data=data.reset_index()
            data=data.reindex(sorting_order)
            data.index=data['id']
            del data['id']
            '''
            print('SUCCESSFULLY ORDERED POINTS!!')
        #ORDERING OF POINTS FINISHED


        #---------------3. INPUT PARAMETERS, ORDER DIM + SELECTED DIM + filtering columns ----------------------------------------------
        # CONVERT JAVASCRIPT OBJECT OF SELECT-COLUMN INTO PYTHON LIST
        dims=[]
        if (selected_dim!=''):
            dims=[s for s in selected_dim.split(' ')]

        # ORDERDIM + SELECT-DIM
        dims=dims+dim

        # REMOVING THE DUPLICATED FROM MERGED LIST
        dims=list(set(dims))
        # FINAL FILTERING THE COLUMNS
        filtered_data=data.loc[:,dims+['classLabel']]
        #print(filtered_data,filtered_data.columns,filtered_data.describe())

        #--------------- 4. BASIC HEIDI IMAGE ---------------------------------------------------------------
        output='static/output'
        matrix,bs,sorted_data=hd.generateHeidiMatrixResults_noorder(output,filtered_data,knn)
        print('----matrix generated ---')
        
        #5-june
        

        img,bit_subspace=hd.generateHeidiMatrixResults_noorder_helper(matrix,bs,output,sorted_data,'legend_heidi')

        output='static/output'
        filename='consolidated_img.png'
        img.save(output+'/'+filename)
        print('--generated image ---')
        
        #lbl=rg.regionLabelling_8(matrix)
        lbl = np.zeros((matrix.shape[0],matrix.shape[1]))
        print('--region labelling done ---')
        
        dbc.deleteAllNodes(labelname=os.path.basename(datasetPath).split('.')[0]+'_heidi')
        dbc.saveMatrixToDatabase_leaf(img,bs,'static/output',sorted_data,lbl,labelname=os.path.basename(datasetPath).split('.')[0]+'_heidi')
        dbc.saveColorToDatabase(bit_subspace,os.path.basename(datasetPath).split('.')[0]+'_heidi')
        filtered_data.to_csv('static/output/sortedData.csv')
        x=list(filtered_data['classLabel'].values)
        #--------------- SAVING IMAGE INFO AND LABEL COLORS, ONE TIME ---------------------------------------------------------------
        dbc.saveClassLabelColorsInDatabase(os.path.basename(datasetPath),list(set(x)))
        l=[]
        label=[]
        for i in set(x):
            c=x.count(i)
            l.append(c)
            label.append(i)
        l=','.join([str(i) for i in l])
        label=','.join([str(i) for i in label])
        dbc.saveInfoToDatabase(img.size[0],img.size[1],os.path.basename(datasetPath),l,label)
        #check above line (WARNING)
        #storing the re-indexed data at output folder
        output='static/output'
        data.to_csv(output+'/sortedData.csv',index=True)
        
        '''
        #--------------- 4B. CLOSED HEIDI IMAGE ---------------------------------------------------------------
        #4-JUNE
        #CODE FOR CREATING CLOSED IMAGE AND SAVING IN DATABASE
        #matrix,bs,sorted_data=hd.generateHeidiMatrixResults_noorder(output,filtered_data,20)
        bm = ch.get_bit_map(filtered_data.shape[1]-1)
        map_dict,_=hh.getMappingDict(matrix,bs)
        matrix,val_map=ch.compress_heidi(matrix,bm)
        print('val_map:',val_map,bs)
        lbl=rg.regionLabelling_8(matrix)
        img,dict1=hd.generateHeidiMatrixResults_noorder_helper(matrix,bs,output,sorted_data,'legend_closed',val_map,map_dict)
        dbc.deleteAllNodes(labelname=os.path.basename(datasetPath).split('.')[0]+'_closed')
        dbc.saveMatrixToDatabase_leaf_v2(img,bs,'static/output',sorted_data,lbl,labelname=os.path.basename(datasetPath).split('.')[0]+'_closed')
        dbc.saveColorToDatabase(dict1,os.path.basename(datasetPath).split('.')[0]+'_closed')
        output='static/output'
        filename='closed_img.png'
        img.save(output+'/'+filename)
        #CLOSED IMAGE CODE END
        
        #--------------- 5. COMPOSITE HEIDI IMAGE ---------------------------------------------------------------
        #5june
        #HEIDI image to composite and saving in database
        color_dict,_=dbc.loadColorFromDatabase(os.path.basename(datasetPath).split('.')[0]+'_heidi')
        temp={}
        for k in color_dict:
            temp[k.replace('H','#')]=color_dict[k]
        print('color_dict',temp,filtered_data)
        img,matrix=hd.createCompositeHeidi(filtered_data,temp,knn=20)
        lbl=rg.regionLabelling_8(matrix)
        dbc.deleteAllNodes(labelname=os.path.basename(datasetPath).split('.')[0]+'_composite')
        dbc.saveMatrixToDatabase_leaf_v2(img,'','static/output',sorted_data,lbl,labelname=os.path.basename(datasetPath).split('.')[0]+'_composite')
        print('saved composite image in database!!')
        output='static/output'
        filename='consolidated_composite.png'
        img.save(output+'/'+filename)
        '''
        #--------------- 6. CLOSED COMPOSITE IMAGE ---------------------------------------------------------------
        '''
        #CLOSED image to composite and saving in database
        color_dict,_=dbc.loadColorFromDatabase(os.path.basename(datasetPath).split('.')[0]+'_closed')
        temp={}
        for k in color_dict:
            temp[k.replace('H','#')]=color_dict[k]
        img,matrix=hd.createCompositeHeidi(filtered_data,temp,knn=20)
        lbl=rg.regionLabelling_8(matrix)
        dbc.deleteAllNodes(labelname=os.path.basename(datasetPath).split('.')[0]+'closed_composite')
        dbc.saveMatrixToDatabase_leaf_v2(img,bs,'static/output',sorted_data,lbl,labelname=os.path.basename(datasetPath).split('.')[0]+'closed_composite')
        print('saved composite image in database!!')
        output='static/output'
        filename='closed_composite.png'
        img.save(output+'/'+filename)
        '''
        '''
        #CODE FOR COMPOSITE IMAGE VISUALIZATION (1-d)
        #img,bs,matrix=hd.generateHeidiMatrixResults_kd(output,filtered_data,1,10) #1 is image type which means 1-d, 2: 2-d ...
        #lbl=rg.regionLabelling_8(matrix)
        #img,dict1=hd.generateHeidiMatrixResults_noorder_helper(matrix,bs,output,sorted_data,'legend_composite')
        #dbc.deleteAllNodes(labelname=os.path.basename(datasetPath).split('.')[0]+'_composite')
        #dbc.saveMatrixToDatabase_leaf_v2(img,bs,'static/output',sorted_data,lbl,labelname=os.path.basename(datasetPath).split('.')[0]+'_composite')
        #dbc.saveColorToDatabase(dict1,os.path.basename(datasetPath).split('.')[0]+'_composite')
        #print('saved composite image in database!!')
        
        '''
        #4-JUNE
        #loading heidi image
        #3sep
        pixels=dbc.databasefilter(labelname=os.path.basename(datasetPath).split('.')[0]+imgType,color='ALL')
        width,height,scale,class_count,class_label=dbc.getImageParams(os.path.basename(datasetPath))
        class_count=class_count.split(',')
        perclustercount=[int(i) for i in class_count]
        class_label=class_label.split(',')
        class_label=[int(i) for i in class_label]
        #print('pppp1',width,height,scale)
        color_dict=dbc.getColorFromTopLegend(os.path.basename(datasetPath))
        #print(color_dict)
        img=dbc.drawImage(pixels,width,height,scale,perclustercount,class_label,color_dict,grid=grid)
        print(os.path.basename(datasetPath))
        dbc.updateImageInfo(img.size[0],img.size[1],os.path.basename(datasetPath)) #LEGEND SPACING AND OTHER STUFF
        output='static/output'
        filename='consolidated_img.png'
        img.save(output+'/'+filename)
        #3sep
        return json.dumps({'output':str("123"),'subspace':str("123")})
    #except Exception as e:
    #    PrintException()
    #    render_template('500.html',error=str(e))



#IF USER CLICKS ON A 'COLOR' IN LEGEND BAR
@mod_heidicontrollers.route('/redrawimg')
def redrawimg():
    print('--redrawing--')
    #INPUT PARAMS FROM WEB PAGE (COLOR VALUE TO BE FILTERED)
    color = request.args.get('color_value')
    datasetName=os.path.basename(request.args.get('datasetPath'))
    grid = request.args.get('grid')
    imgType = request.args.get('imgType')
    id1 = '' #warning check once
    if(grid=='yes'): grid=True
    else: grid=False
    print('color value:',color,imgType,grid)
    return ""

#IF USER CLICKS ON A PIXEL IN IMAGE, THIS METHOD IS CALLED
@mod_heidicontrollers.route('/highlightPattern')
def highlightPattern():
    print('-- highlightPattern-- ')
    x = float(request.args.get('x'))
    y = float(request.args.get('y'))
    id1 = request.args.get('id')
    grid=request.args.get('grid')
    gridPatterns=request.args.get('gridPatterns')
    if grid=='yes': grid=True
    else: grid=False
    if gridPatterns=='yes': gridPatterns=True
    else: gridPatterns=False
    print('grid',grid,gridPatterns)
    imgType = '_'+request.args.get('imgType')
    datasetPath = 'static/output'
    datasetName = 'image'
    print(x,y,datasetPath,datasetName)
    datasetName=os.path.basename(request.args.get('datasetPath'))
    width,height,scale,class_count,class_label=dbc.getImageParams(datasetName)
    

    tx = ImageInfo.query.filter_by(name=datasetName)
    w,h=tx[0].with_legend_width,tx[0].with_legend_height
    class_count=class_count.split(',')
    perclustercount=[int(i) for i in class_count]
    class_label=class_label.split(',')
    class_label=[int(i) for i in class_label]
    x=(x*w)/(scale)
    y=(y*h)/(scale)
    #print(x-1,y-1)
    x=int(math.ceil(x))
    y=int(math.ceil(y))
    t=y
    y=x
    x=t
    print(x,y,datasetName.split('.')[0]+imgType)
    tlx,tly,block_row,block_col=dbc.getTopLeftCoordinates_Grid(x-1,y-1,labelname=datasetName.split('.')[0]+imgType, datasetName=datasetName)
    print('TOP lEFT COORDINATES: ',tlx,tly)
    
    if(gridPatterns==True):
        pixels,color=dbc.blockfilter(x-1,y-1,labelname=datasetName.split('.')[0]+imgType)
    else:
        pixels,color=dbc.databasepatternfilter(x-1,y-1,labelname=datasetName.split('.')[0]+imgType)

    
    #subspace=dbc.getColorSubspace(color,datasetName.split('.')[0]+imgType)
    print(color)
    tx=Legend.query.filter_by(name=datasetName.split('.')[0]+imgType,color=color[1:])

    print('subspaceeee',tx[0].subspace)
    
    #img=rg.visualize_regions_v2(pixels,width,height,scale)
    
    width,height,scale,class_count,class_label=dbc.getImageParams(datasetName)
    class_count=class_count.split(',')
    perclustercount=[int(i) for i in class_count]
    class_label=class_label.split(',')
    class_label=[int(i) for i in class_label]
    #print('pppp1',width,height,scale)
    color_dict=dbc.getColorFromTopLegend(datasetName)
    print('color_dict',color_dict)    
    img = dbc.drawImage(pixels,width,height,scale,perclustercount,class_label,color_dict,grid=grid)
    background = dbc.getbackground(datasetName.split('.')[0]+imgType,datasetName,grid=grid)
    background.save('static/output/background.png')
    img.save('static/output/img.png')
    
    img = ImageChops.multiply(background,img)
    #img=dbc.mergeImage(background,img)
    output='static/output'
    filename='temp'+imgType+'.png'
    img.save(output+'/'+filename)
    #sortedData=pd.read_csv('static/output/sortedData.csv',index_col='id')
    sortedPath='static/output/sortedData.csv'
    rp,cp=dbc.getCoordinates(pixels,sortedPath,unique=True)
    print(rp,cp)
    rp.to_csv('static/output/rowPoints.csv')
    cp.to_csv('static/output/colPoints.csv')
    #return json.dumps({})

    return json.dumps({'path':output+'/'+filename, 'rowPoints':rp.reset_index().to_json(orient='records'),'colPoints':cp.reset_index().to_json(orient='records')})


@mod_heidicontrollers.route('/resetImage')
def resetImage():
    print('-- Reset Image ---')
    datasetPath = request.args.get('datasetPath')
    grid = request.args.get('grid')
    imgType='_'+request.args.get('imgType')
    print('imgType',imgType)
    if(grid=='yes'): grid=True
    else: grid=False
    #CALLING COLOR FILTER CODE
    start=time.time()
    pixels=dbc.databasefilter(labelname=os.path.basename(datasetPath).split('.')[0]+imgType,color='ALL')
    end=time.time()
    #print('\t 1. pixels retrieved from database. Its count is %d , total time taken is %f sec' %(len(pixels),(end-start)))
    width,height,scale,class_count,class_label=dbc.getImageParams(os.path.basename(datasetPath))
    color_dict=dbc.getColorFromTopLegend(os.path.basename(datasetPath))
    class_count=class_count.split(',')
    perclustercount=[int(i) for i in class_count]
    class_label=class_label.split(',')
    class_label=[int(i) for i in class_label]
    img=dbc.drawImage(pixels,width,height,scale,perclustercount,class_label,color_dict,grid=grid)
    print('\t 2. created image')
    dbc.updateImageInfo(img.size[0],img.size[1],os.path.basename(datasetPath)) # JUST TO BE EXTRA PRECAUTIOUS
    output='static/output'
    filename='consolidated_img.png'
    img.save(output+'/'+filename)

    print('\t 3. Returing the created image')
    _,subspace=dbc.loadColorFromDatabase(os.path.basename(datasetPath).split('.')[0]+imgType) #SUBSPACE RETURNED IS LIST OF LISTS
    print('subspace',str(subspace))
    return json.dumps({'output':output,'subspace':subspace})
