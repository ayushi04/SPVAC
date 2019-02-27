import base64
import StringIO
from app import db, login_manager
import random
import os
import pandas as pd
import config
import time
import matplotlib.pyplot as plt

from mod_dim import best_heidi_img as hd
from mod_dim import heidiHelper as hh
from mod_dim import first
from mod_dim import orderPoints as op
from mod_dim import compressed_heidi as ch
from mod_dim import bea2
from mod_dim import region_label as rg
from mod_dim import database_connectivity_v1 as dbc
import math
import json
import ast
from mod_dim import jaccardMatrix as jm
from mod_dim import report_generator_helper as rgh

import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Panel, Tabs
from bokeh.layouts import gridplot



def subspace_all(datasetPath,grid):

    # READING THE DATASET
    data=pd.read_csv(filepath_or_buffer=datasetPath,sep=',',index_col='id')

    #save 2^d-1 colors in database with subspace
    cname=list(data.columns)
    cname.pop(0)
    subspaceDict = hd.getAllSubspace(data.columns)
    
    dbc.saveColorToDatabase(subspaceDict,os.path.basename(datasetPath).split('.')[0]+'_exp')

    color_dict,_=dbc.loadColorFromDatabase(os.path.basename(datasetPath).split('.')[0]+'_exp')
    
    temp={}
    for k in color_dict:
        temp[k.replace('H','#')]=color_dict[k]
    
    imgDict,bitmask,subspaceList,colorList = hd.createCompositeExp(data,temp,knn=20)

    print(subspaceList)

    
    output_file('image.html')

    c_dim = data.shape[1]-1 #count of dimensions in dataset, (-1) for classLabel
    dim2=list(data.columns)
    dim2.pop(-1)

    tabs=[]
    for c in dim2:
        dim=list(data.columns)
        dim.pop(-1)
        row=0
        matrix = [[None for _ in range(c_dim)] for _ in range(c_dim)]
        k=0
        start=[c]
        dim.remove(c)
        idx=subspaceList.index(set(start))
        matrix[row][k]=visualizeImg(bitmask[idx],colorList[idx],start)#bitmask[st]
        while (len(dim)>0):
            st=start
            #idx=subspaceList.index(st)
            #matrix[row][k]=str(st)#bitmask[st]
            col=1+row
            for i in dim:
                st=st+[i]
                idx=subspaceList.index(set(st))
                #matrix[row][col]=bitmask[idx]#str(st)
                matrix[row][col]=visualizeImg(bitmask[idx],colorList[idx],st)
                col=col+1
            row=row+1
            dim.pop(0)
            k=k+1
        tabs = tabs + [ Panel(child=gridplot(matrix),title=c) ]
    
    tabs = Tabs(tabs=tabs)
    return tabs

    #show(matrix[0][1])
    #print(matrix[0][1])
    #show(gridplot(matrix))

    '''
    p1 = figure(plot_width=300, plot_height=300)
    p1.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)
    tab1 = Panel(child=p1, title="circle")

    p2 = figure(plot_width=300, plot_height=300)
    p2.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=3, color="navy", alpha=0.5)
    p3 = figure(plot_width=300, plot_height=300)
    p3.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=3, color="navy", alpha=0.5)
    tab2 = Panel(child=row([p2,p3]), title="line")

    tabs = Tabs(tabs=[ tab1, tab2 ])
    '''
    

def visualizeImg(img,color,subspace):
    print(color)
    data = dict(image=[img],
                #squared=[ramp**2, steps**2, bitmask**2],
                pattern=['bitmask'],
                x=[0],
                y=[0],
                dw=[5],
                dh=[5]
                )

    TOOLTIPS = [
        ('index', "$index"),
        ('pattern', '@pattern'),
        ("x", "$x"),
        ("y", "$y"),
        ("value", "@image"),
        ('squared', '@squared')
    ]

    p = figure( title=str(subspace),x_range=(0, 5), y_range=(0, 5), tools='hover,wheel_zoom',width=250, plot_height=250, x_axis_location='above', y_axis_location='left')
    p.image(source=data, image='image', x='x', y='y', dw='dw', dh='dh', palette=[color,'#ffffff'])
    p.xaxis.visible = False 
    p.yaxis.visible = False 
    return p

    '''
    plist=[]
    for  b,k in zip(bitmask,imgDict.keys()):
        data = dict(image=[b],
                    #squared=[ramp**2, steps**2, bitmask**2],
                    pattern=['bitmask'],
                    x=[0],
                    y=[0],
                    dw=[5],
                    dh=[5]
                    )

        TOOLTIPS = [
            ('index', "$index"),
            ('pattern', '@pattern'),
            ("x", "$x"),
            ("y", "$y"),
            ("value", "@image"),
            ('squared', '@squared')
        ]

        p = figure( x_range=(0, 5), y_range=(0, 5), tools='hover,wheel_zoom',width=250, plot_height=250, x_axis_location='above', y_axis_location='left')
        p.image(source=data, image='image', x='x', y='y', dw='dw', dh='dh', palette=[k,'#ffffff'])
        plist=plist+[p]

    from bokeh.layouts import row

    show(row(plist))
    '''
    return "hello"
	
def analyticsReport_helper(datasetPath,imgType):

    print('-----analyticsReport_helper-----------')
    datasetName=os.path.basename(datasetPath)
    # READING THE DATASET
    data=pd.read_csv(filepath_or_buffer=datasetPath,sep=',',index_col='id')
    
    rowBlockId=0
    colBlockId=[1,2]
    colId=0
    w,h=dbc.getBlockDimension(datasetName,rowBlockId,colBlockId[colId])
    w_g2,h_g2=dbc.getBlockDimension(datasetName,rowBlockId,colBlockId[colId+1])
    id1=''
    width,height,scale,class_count,class_label=dbc.getImageParams(datasetName) #img width, img height stored in database (no legend)
    tlx,tly=dbc.getTopLeft_usingBlockId(0,colBlockId[colId],labelname=datasetName.split('.')[0],imgType=imgType+id1)
    tlx_g2,tly_g2=dbc.getTopLeft_usingBlockId(0,colBlockId[colId+1],labelname=datasetName.split('.')[0],imgType=imgType+id1)
    print('tlx and tly, scale:',tlx,tly,scale)
    
    #1. get all pixels for block[0,1]
    pixels_c1=dbc.getBlockPatternsColor(datasetName,colBlockId[colId],rowBlockId,color_val='ALL',imgType=imgType)
    pixels_c2=dbc.getBlockPatternsColor(datasetName,colBlockId[colId+1],rowBlockId,color_val='ALL',imgType=imgType)
    
    img=dbc.drawPattern(pixels_c1,w,h,5,grid=False,topLeft_x=tly,topLeft_y=tlx)
    img_grid2=  dbc.drawPattern(pixels_c2,w_g2,h_g2,10,grid=False,topLeft_x=tly_g2,topLeft_y=tlx_g2)
    #blockImage
    output = StringIO.StringIO()
    img.save(output, format='PNG')
    output.seek(0)
    output_s = output.read()
    blockImage = base64.b64encode(output_s)
    output = StringIO.StringIO()

    img_grid2.save("static/output/grid2.png")

    img_grid2.save(output, format='PNG')
    output.seek(0)
    output_s = output.read()
    blockImage2 = base64.b64encode(output_s)
    
    #2. get all unique color values
    colors = [i.getColor() for i in pixels_c1]
    colors = list(set(colors))
    if('#ffffff' in colors):
        colors.remove('#ffffff')

    #3. for each color get rowPoints and colPoints
    newImages=[]
    for color in colors:
        rowImgPoints=[]
        colImgPoints=[]
        pixels_color=[]
        for pixel in pixels_c1:
            if(pixel.getColor()==color):
                rowImgPoints=rowImgPoints+pixel.getRowImgPoints()
                colImgPoints=colImgPoints+pixel.getColImgPoints()
                rowImgPoints = list(set(rowImgPoints))
                colImgPoints = list(set(colImgPoints))
                pixels_color = pixels_color + [pixel]
        print(len(rowImgPoints),len(colImgPoints))
        

        img=dbc.drawPattern(pixels_color,w,h,scale,grid=False,topLeft_x=tly,topLeft_y=tlx)
        #img.save("static/output/image_pattern"+color[1:]+".png")
        newimg,removed_rows=rgh.filterColsFromImage(img)
        newimg,removed_cols=rgh.filterRowsFromImage(newimg)
        newimg=rgh.annotateImage(newimg,scale,colImgPoints,rowImgPoints)
        #newimg.save("static/output/image_pattern_reduced"+color[1:]+".png")
        output = StringIO.StringIO()
        newimg.save(output, format='PNG')
        output.seek(0)
        output_s = output.read()
        b64 = base64.b64encode(output_s)
        newimg_g2=rgh.filterRowsFromImage_givenrows(img_grid2,removed_cols)
        newimg_g2=rgh.annotateImage(newimg_g2,scale,colImgPoints,[])
        output = StringIO.StringIO()
        newimg_g2.save(output, format='PNG')
        output.seek(0)
        output_s = output.read()
        b64_g2 = base64.b64encode(output_s)
        

        newImages = newImages + [{'image':b64,'grid2Images':b64_g2}]

        #newimg,removed_rows=rgh.filterRowsFromImage(img)
        #newimg=rgh.annotateImage(newimg,scale,colImgPoints)
        #newimg.save("static/output/image_pattern_reduced"+color[1:]+".png")

        #4. in third block, get image for row pixels in step one
        #pixels_c1=dbc.getBlockPatternsColor(datasetName,rowBlockId,colBlockId[1],color_val='ALL')       



    #5. visualize filtered row 3rd block as image
    #6. get all unique colors in reduced 3rd block
    #7. for each color, get rowPoints and colImgPoints

    return newImages,blockImage
    return [],blockImage


