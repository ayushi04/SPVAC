import seaborn as sns
import pandas as pd
import numpy as np
import math
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import operator
from PIL import Image
import sys
import webcolors as wb
#import  heidiHelper as hh
#import orderPoints as op
#import compressed_heidi as ch

from mod_dim import  heidiHelper as hh
from mod_dim import orderPoints as op
#from mod_dim import compressed_heidi as ch
from mod_dim import database_connectivity as dbc
knn=50
# for Box-Cox Transformation
#from scipy import stats
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler,MinMaxScaler

def normalize_data(inputData):
    '''
    for col in range(inputData.shape[1]):
        if(col=='id' or col=='classLabel'): continue
        scaler = StandardScaler()
        scaler.fit(inputData.iloc[:,col])
        inputData.iloc[:,col]=scaler.transform(inputData.iloc[:,col])
    '''
    col=list(inputData.columns)
    if('id' in col): col.remove('id')
    if('classLabel' in col): col.remove('classLabel')
    t=inputData.loc[:,col]
    scaler = MinMaxScaler()#StandardScaler()
    scaler.fit(t)
    inputData.loc[:,col]=scaler.transform(t)
    return inputData


def get_all_kd_subspaces(k,dims):
    max_count=int(math.pow(2,dims))
    allsubspaces=range(1,max_count)
    f=lambda a:sorted(a,key=lambda x:sum(int(d)for d in bin(x)[2:]))
    allsubspaces=f(allsubspaces)
    print('xxx',allsubspaces)
    frmt=str(dims)+'b'
    factor=1
    bit_map={}
    subspace_map={}
    count=0
    subspaces=[x for x in allsubspaces if sum(int(d)for d in bin(x)[2:])==k]
    return subspaces

def generateHeidiMatrixResults_test4(outputPath,inputData,k):
    global global_count,global_map_dict
    create_empty_folder(outputPath)
    global_count = 0
    factor=1
    bit_subspace={}
    row=inputData.shape[0]
    count=0
    heidi_matrix=np.zeros(shape=(row,row),dtype=np.uint64)
    allsubspaces=get_all_kd_subspaces(k,inputData.shape[1]-1)
    print(allsubspaces)
    print('knn:',knn)
    for col in range(0,inputData.shape[1]-1):
        filtered_data=inputData.iloc[:,[col,-1]] #NEED TO CHANGE IF COL IS A LIST
        param={}
        param['columns']=list(filtered_data.columns[:-1])
        param['order']=[True for i in param['columns']]
        sorted_data=op.sortbasedOnclassLabel(filtered_data,'dimension',param)
        subspace=sorted_data.iloc[:,:-1]
        np_subspace=subspace.values#NEED TO CHANGE IF COL IS A LIST
        #print(np_subspace.shape)
        nbrs=NearestNeighbors(n_neighbors=knn,algorithm='ball_tree').fit(np_subspace)
        temp=nbrs.kneighbors_graph(np_subspace).toarray()
        temp=temp.astype(np.uint64)
        heidi_matrix=heidi_matrix + temp*factor
        factor=factor*2
        bit_subspace[count]=col
        count+=1

    map_dict,all_info=hh.getMappingDict(heidi_matrix,bit_subspace)
    hh.createLegend(map_dict,all_info,outputPath+'/legend.html')
    img,imgarray=hh.generateHeidiImage(heidi_matrix,map_dict)
    hh.saveHeidiImage(img,outputPath,'img_bea.png')

    array=sorted_data['classLabel'].value
    algo1_bar,t=hh.createBar(array)
    hh.visualizeConsolidatedImage(imgarray,algo1_bar,outputPath+'/consolidated_img.png')
    print('visualized consolidated image')

#best image (no ordering) (k length subspaces)
def generateHeidiMatrixResults_kd(outputPath,inputData,k,knn=knn):
    global global_count,global_map_dict
    #hh.create_empty_folder(outputPath)
    global_count = 0
    factor=1
    bit_subspace={}
    row=inputData.shape[0]
    count=0
    print('hello',k)
    heidi_matrix=np.zeros(shape=(row,row),dtype=np.uint64)
    allsubspaces=get_all_kd_subspaces(k,inputData.shape[1]-1)
    print('allsubspaces',allsubspaces)
    frmt=str(inputData.shape[1]-1)+'b'
    factor=1
    bit_subspace={}
    count=0
    print('knn:',knn)

    #for col in range(0,inputData.shape[1]-1):
    #hh.create_empty_folder(outputPath+'/t1')
    for i in allsubspaces:
        bin_value=str(format(i,frmt))
        bin_value=bin_value[::-1]
        subspace_col=[index for index,value in enumerate(bin_value) if value=='1']

        filtered_data=inputData.iloc[:,subspace_col+[-1]] #NEED TO CHANGE IF COL IS A LIST
        filtered_data['classLabel_orig']=filtered_data['classLabel'].values
        #param={}
        #param['columns']=list(filtered_data.columns[:-1])
        #param['order']=[True for i in param['columns']]
        if k==1:
            param={}
            param['columns']=list(filtered_data.columns[:-1])
            param['order']=[True for i in param['columns']]
            ordering='dimension'
        else:
            param={}
            ordering='mst_distance'
        sorted_data=op.sortbasedOnclassLabel(filtered_data,ordering,param)
        subspace=sorted_data.iloc[:,:-2]
        np_subspace=subspace.values#NEED TO CHANGE IF COL IS A LIST
        #print(np_subspace.shape)
        nbrs=NearestNeighbors(n_neighbors=knn,algorithm='ball_tree').fit(np_subspace)
        temp=nbrs.kneighbors_graph(np_subspace).toarray()
        temp=temp.astype(np.uint64)
        heidi_matrix=heidi_matrix + temp*factor
        temp=temp*factor
        factor=factor*2
        #bit_subspace[count]=subspace_col
        subspace_col_name=[inputData.columns[i] for i in subspace_col]
        print(subspace_col_name)
        bit_subspace[count]=subspace_col_name
        count+=1
        #map_dict,all_info=hh.getMappingDict(temp,bit_subspace,count-1)
        #hh.createLegend(map_dict,all_info,outputPath+'/t1/legend'+str(count)+'.html')
        #img,imgarray=hh.generateHeidiImage(temp,map_dict)
        #hh.saveHeidiImage(img,outputPath,'/t1/img_bea'+str(count)+'.png')
        #array=sorted_data['classLabel'].values
        #algo1_bar,t=hh.createBar(array)
        #hh.visualizeConsolidatedImage(imgarray,algo1_bar,outputPath+'/t1/consolidated_img'+str(count)+'.png')
    #count=0
    map_dict,all_info=hh.getMappingDict(heidi_matrix,bit_subspace,count)
    hh.createLegend(map_dict,all_info,outputPath+'/legend.html')
    img,imgarray=hh.generateHeidiImage(heidi_matrix,map_dict)
    hh.saveHeidiImage(img,outputPath,'img_bea.png')

    array=sorted_data['classLabel'].values
    print(array)
    algo1_bar,t=hh.createBar(array)
    hh.visualizeConsolidatedImage(imgarray,algo1_bar,outputPath+'/consolidated_img.png')
    print('visualized consolidated image')
    return img,bit_subspace,heidi_matrix

def generateHeidiMatrixResults_noorder_subspace(outputPath,inputData,k=20):
    hh.create_empty_folder(outputPath)
    knn=k
    print('knn:',knn)
    subspace=inputData.iloc[:,:-1]
    np_subspace=subspace.values#NEED TO CHANGE IF COL IS A LIST
    nbrs=NearestNeighbors(n_neighbors=knn,algorithm='ball_tree').fit(np_subspace)
    heidi_matrix=nbrs.kneighbors_graph(np_subspace).toarray()
    heidi_matrix=heidi_matrix.astype(np.uint64)
    return heidi_matrix


def generateHeidiMatrixResults_noorder(outputPath,inputData,k=20):
    hh.create_empty_folder(outputPath)
    factor=1
    knn=k
    bit_subspace={}
    row=inputData.shape[0]
    count=0
    heidi_matrix=np.zeros(shape=(row,row),dtype=np.uint64)
    max_count=int(math.pow(2,inputData.shape[1]-1))
    allsubspaces=range(1,max_count)
    f=lambda a:sorted(a,key=lambda x:sum(int(d)for d in bin(x)[2:]))
    allsubspaces=f(allsubspaces)
    print(allsubspaces)
    frmt=str(inputData.shape[1]-1)+'b'
    factor=1
    bit_subspace={}
    count=0
    print('knn:',knn)

    for i in allsubspaces:
        bin_value=str(format(i,frmt))
        bin_value=bin_value[::-1]
        subspace_col=[index for index,value in enumerate(bin_value) if value=='1']

        filtered_data=inputData.iloc[:,subspace_col+[-1]] #NEED TO CHANGE IF COL IS A LIST
        filtered_data['classLabel_orig']=filtered_data['classLabel'].values
        sorted_data=filtered_data
        subspace=sorted_data.iloc[:,:-2]
        np_subspace=subspace.values#NEED TO CHANGE IF COL IS A LIST
        #print(np_subspace.shape)
        nbrs=NearestNeighbors(n_neighbors=knn,algorithm='ball_tree').fit(np_subspace)
        temp=nbrs.kneighbors_graph(np_subspace).toarray()
        temp=temp.astype(np.uint64)
        heidi_matrix=heidi_matrix + temp*factor
        factor=factor*2
        subspace_col_name=[inputData.columns[j] for j in subspace_col]
        print(i,subspace_col_name)
        bit_subspace[count]=subspace_col_name
        count+=1
    return heidi_matrix,bit_subspace,sorted_data



def generateHeidiMatrixResults_noorder_helper(heidi_matrix,bit_subspace,outputPath,sorted_data,legend_name,val_map={},mapping_dict={}):
    if(val_map=={}) : map_dict,all_info=hh.getMappingDict(heidi_matrix,bit_subspace)
    else:
        #map_dict,all_info=hh.getMappingDict(heidi_matrix,bit_subspace)
        map_dict,all_info=hh.getMappingDictClosedImg(heidi_matrix,bit_subspace,val_map,mapping_dict)

    print(map_dict,all_info)
    
    hh.createLegend(map_dict,all_info,outputPath+'/'+legend_name+'.html')
    
    dict1=hh.dictForDatabase(map_dict,all_info)
    img,imgarray=hh.generateHeidiImage(heidi_matrix,map_dict)
    print('1-------------------------------------------------------')
    hh.saveHeidiImage(img,outputPath,'img_bea.png')
    print('2-------------------------------------------------------')
    array=sorted_data['classLabel'].values
    print('3-------------------------------------------------------')
    algo1_bar,t=hh.createBar(array)
    hh.visualizeConsolidatedImage(imgarray,algo1_bar,outputPath+'/consolidated_img.png')
    print('visualized consolidated image')
    
    return img,dict1


def createCompositeExp(inputData,subspaceDict,knn=knn):
    print('----createCompositeHeidi----')

    #INITIALIZING THE HEIDI MATRIX
    row=inputData.shape[0]
    heidi_matrix=np.zeros(shape=(row,row),dtype=np.uint64)
    imgDict={}
    bitmask=[]
    subspaceList=[]
    colorList=[]
    #factor=1
    j=1
    print(subspaceDict)
    #FOR EACH COLOR IN SUBSPACE DICTIONARY
    for color in subspaceDict:
        allsubspace=subspaceDict[color][0]
        #1. SORTING AND FILTERING THE DATA
        if len(allsubspace)==1:
            param={}
            param['columns']=allsubspace
            param['order']=[True for i in param['columns']]
            ordering='dimension'
        else:
            param={}
            #ordering='pca_ordering'
            #ordering='euclidian_distance'
            ordering='knn_bfs'
            #ordering='mst_distance'
        #print(allsubspace,ordering)
        filtered_data=inputData[allsubspace+['classLabel']]
        filtered_data['classLabel_orig']=filtered_data['classLabel'].values
        
        #print(filtered_data)
        sorted_data=op.sortbasedOnclassLabel(filtered_data,ordering,param)
        
        #SELECTING COLUMNS OF INPUT DATA BASED ON SUBSPACE
        filtered_data=sorted_data[allsubspace]
        subspace=filtered_data
        np_subspace=subspace.values#NEED TO CHANGE IF COL IS A LIST
        
        #CREATING KNN MATRIX
        nbrs=NearestNeighbors(n_neighbors=knn,algorithm='ball_tree').fit(np_subspace)
        hm=nbrs.kneighbors_graph(np_subspace).toarray()
        temp=np.flip(hm,0)
        
        bitmask=bitmask+[temp==0]
        subspaceList=subspaceList+[set(allsubspace)]

        colorList=colorList+[color]
        hm=hm.astype(np.uint64)

        img,_=hh.generateHeidiImage_hex(hm,{1:color})
        hh.saveHeidiImage(img,'static/output_exp','img'+str(j)+'.png')
        j=j+1
        imgDict[color]=img
        

    return imgDict,bitmask,subspaceList,colorList

def createCompositeHeidi(inputData,subspaceDict,knn=knn):  
    print('----createCompositeHeidi----')
    bit_subspace={}
    row=inputData.shape[0]
    heidi_matrix=np.zeros(shape=(row,row),dtype=np.uint64)
    factor=1
    f=0
    for color in subspaceDict:
        print(color)
        
        #1. GET SORTED DATA FOR EACH COLOR
        allsubspace=[]
        for subspace in subspaceDict[color]:
            allsubspace=allsubspace+subspace
        allsubspace=list(set(allsubspace))
        #print(allsubspace,len(allsubspace))
        if len(allsubspace)==1:
            param={}
            param['columns']=allsubspace
            param['order']=[True for i in param['columns']]
            ordering='dimension'
        else:
            param={}
            #ordering='pca_ordering'
            #ordering='euclidian_distance'
            ordering='mst_distance'
        filtered_data=inputData[allsubspace+['classLabel']]
        filtered_data['classLabel_orig']=filtered_data['classLabel'].values
        sorted_data=op.sortbasedOnclassLabel(filtered_data,ordering,param)
        print(sorted_data.shape)
        hm=np.zeros(shape=(row,row),dtype=np.uint64)
        c=0
        for subspace in subspaceDict[color]:
            filtered_data=sorted_data[subspace]
            subspace=filtered_data
            np_subspace=subspace.values#NEED TO CHANGE IF COL IS A LIST
            #print(np_subspace.shape)
            nbrs=NearestNeighbors(n_neighbors=knn,algorithm='ball_tree').fit(np_subspace)
            temp=nbrs.kneighbors_graph(np_subspace).toarray()
            temp=temp.astype(np.uint64)
            if c==0: hm=hm | temp
            else: hm =hm & temp 
        #print(hm,factor*hm)
        heidi_matrix=heidi_matrix+factor*hm
        bit_subspace[f]=color#subspaceDict[color]#color
        f=f+1
        #bit_subspace[factor]=color#subspaceDict[color]#color
        factor=factor*2
        #if(color=='#7092ec'): break
    t=np.unique(heidi_matrix)
    #t=[bin(i) for i in t]
    comp_dict={}
    for k in range(len(t)):
        bin_value=bin(t[k])[::-1]
        subspace_col=[index for index,value in enumerate(bin_value) if value=='1']
        val=[]
        for x in subspace_col:
            val=val+[bit_subspace[x]]
        import itertools
        val.sort()
        comp_dict[t[k]]=list(val for val,_ in itertools.groupby(val))
        #print(t[k],bin(t[k]),subspace_col,val)
    
    import webcolors as wb
    arr=np.zeros((heidi_matrix.shape[0],heidi_matrix.shape[1],3))
    #color_map={}
    #color_rev_map={}
    #new_color_map={}
    for i in range(heidi_matrix.shape[0]):
        for j in range(heidi_matrix.shape[1]):
            x=comp_dict[heidi_matrix[i][j]]
            if len(x)==1:
                arr[i][j]=list(wb.hex_to_rgb(x[0]))
            elif(len(x)!=0):
                #print(x)
                x=[list(wb.hex_to_rgb(x)) for x in comp_dict[heidi_matrix[i][j]]]
                new_color=tuple([ int(sum(row[i] for row in x)/len(x)) for i in range(3) ])
                arr[i][j]=list(new_color)
                #if not new_color in new_color_map: new_color_map[wb.rgb_to_hex(new_color)]=1 
                #else:
                #    print('else called')
                #    new_color_map[wb.rgb_to_hex(new_color)]=new_color_map[wb.rgb_to_hex(new_color)]+1
                #color_map[wb.rgb_to_hex(new_color)]=comp_dict[heidi_matrix[i][j]]
                #for k in comp_dict[heidi_matrix[i][j]]:
                #    if not k in color_rev_map:
                #        color_rev_map[k]=set([wb.rgb_to_hex(new_color)])
                #    else:
                #        color_rev_map[k]=color_rev_map[k].union([wb.rgb_to_hex(new_color)])
            else: arr[i][j]=[255,255,255]

    tmp=arr.astype(np.uint8)
    img_top100 = Image.fromarray(tmp)  
    img_top100.save('cmp.png')     
    return img_top100  ,heidi_matrix  
          

#input : ['a', 'b', 'c', 'd', 'classLabel']
#return : {' 0bfff': ['a'], '94 0d3': ['b'], '4169e1': ['c'], '7092ec': ['d'], 'ffd7 0': ['a', 'b'], 'a52a2a': ['a', 'c'], '3e5617': ['b', 'c'], 'f13f7a': ['a', 'd'], 'bea927': ['b', 'd'], 'd99bbb': ['c', 'd'], '33626b': ['a', 'b', 'c'], '7636 e': ['a', 'b', 'd'], '47bec0': ['a', 'c', 'd'], 'e39366': ['b', 'c', 'd'], '76b465': ['a', 'b', 'c', 'd']}
def getAllSubspace(column_names):
    print('--best_heidi_image : getAllSubspace--')
    cname=column_names
    max_count=int(math.pow(2,len(cname)-1))
    allsubspaces=range(1,max_count)
    f=lambda a:sorted(a,key=lambda x:sum(int(d)for d in bin(x)[2:]))
    allsubspaces=f(allsubspaces)
    frmt=str(len(cname)-1)+'b'
    
    color_list = [ [255,69,0],[0,191,255],[148,0,211],[255,215,0],[65,105,225],[165,42,42],[62,86,23],[51,98,107],  [112,146,236],  [241,63,122],  [190,169,39],  [118,54,14],  [217,155,187],  [71,190,192],  [227,147,102],  [118,180,101],  [159,47,132],  [216,133,224],  [107,78,181],  [174,37,43],  [73,98,152],  [232,127,43],  [194,103,105],  [97,177,216],  [170,121,34],  [163,165,86],  [56,103,72],  [54,158,43],  [86,59,28],  [224,57,163],  [177,95,231],  [232,102,155],  [95,188,156],  [156,91,152],  [117,45,66],  [114,119,28],  [161,69,179],  [69,69,86],  [167,110,81],  [150,167,219],  [131,47,44],  [62,143,155],  [128,106,143],  [234,93,83],  [230,100,220],  [191,153,224],  [195,154,89],  [99,85,21],  [228,157,51],  [169,54,77],  [73,62,122],  [193,98,71],  [115,43,104],  [131,112,234],  [125,195,50],  [188,48,20],  [222,53,85],  [168,51,109],  [99,128,154],  [134,157,43],  [46,107,25],  [226,105,185],  [70,192,134],  [174,114,139],  [134,180,193],  [75,149,213],  [70,187,98],  [232,47,190],  [236,60,58],  [34,74,67],  [158,110,200],  [232,102,119],  [59,132,121],  [66,111,214],  [78,128,73],  [233,44,138],  [128,120,61],  [149,94,36],  [166,145,190],  [96,105,180],  [88,159,115],  [50,76,111],  [218,125,167],  [238,142,139],  [186,50,166],  [94,64,146],  [169,185,45],  [155,61,26],  [115,62,44],  [69,74,32],  [200,161,68],  [209,99,43],    [95,135,50],  [105,165,49],  [237,122,97],  [37,77,33],  [161,186,94],  [64,206,71],  [122,80,102],  [202,44,105],  [115,82,40]  ];
    
    colorDict={}
    for i in allsubspaces:
        if(i==len(color_list)): return 'ERROR: best_heidi_image : getAllSubspace, number of subspaces are greater than number of unique color '
        bin_value=str(format(i,frmt))
        bin_value=bin_value[::-1]
        subspace_col=[index for index,value in enumerate(bin_value) if value=='1']
        #hexval= '%2x%2x%2x' %(tuple(color_list[i]))
        hexval=wb.rgb_to_hex(tuple(color_list[i]))[1:]
        colorDict[hexval] = [column_names[idx] for idx in subspace_col]

    return colorDict

#subspaceDict={color:subspace}
#OLD
def createCompositeHeidi_v1(inputData,subspaceDict,knn=knn):  
    print('createCompositeHeidi:',subspaceDict)
    bit_subspace={}
    row=inputData.shape[0]
    heidi_matrix=np.zeros(shape=(row,row),dtype=np.uint64)
    factor=1
    for color in subspaceDict:
        print(color)
        
        #1. GET SORTED DATA FOR EACH COLOR
        allsubspace=[]
        for subspace in subspaceDict[color]:
            allsubspace=allsubspace+subspace
        allsubspace=list(set(allsubspace))
        #print(allsubspace,len(allsubspace))
        if len(allsubspace)==1:
            param={}
            param['columns']=allsubspace
            param['order']=[True for i in param['columns']]
            ordering='dimension'
        else:
            param={}
            #ordering='pca_ordering'
            ordering='euclidian_distance'
            #ordering='mst_distance'
        filtered_data=inputData[allsubspace+['classLabel']]
        filtered_data['classLabel_orig']=filtered_data['classLabel'].values
        sorted_data=op.sortbasedOnclassLabel(filtered_data,ordering,param)
        #print(allsubspace,sorted_data)
        #2. GENERATING HEIDI MATRIX FOR EACH COLOR
        hm=np.zeros(shape=(row,row),dtype=np.uint64)
        c=0
        for subspace in subspaceDict[color]:
            filtered_data=sorted_data[subspace]
            subspace=filtered_data
            np_subspace=subspace.values#NEED TO CHANGE IF COL IS A LIST
            #print(np_subspace.shape)
            nbrs=NearestNeighbors(n_neighbors=knn,algorithm='ball_tree').fit(np_subspace)
            temp=nbrs.kneighbors_graph(np_subspace).toarray()
            temp=temp.astype(np.uint64)
            if c==0: hm=hm | temp
            else: hm =hm & temp 
        #print(hm,factor*hm)
        heidi_matrix=heidi_matrix+factor*hm
        bit_subspace[factor]=color#subspaceDict[color]#color
        factor=factor*2
        #print(factor,allsubspace)
        #print('-----GENERATEiMAGE : generateHeidiImage ------')
        print(bit_subspace,subspaceDict)
        arr=np.zeros((hm.shape[0],hm.shape[1],3))
        for i in range(hm.shape[0]):
            for j in range(hm.shape[1]):
                if hm[i][j] in bit_subspace.keys():
                    arr[i][j]=list(wb.hex_to_rgb(color))
                else:
                    arr[i][j]=[255,255,255]
        # DEBUG IMAGE, ORDEING OF POINTS
        '''
        tmp=arr.astype(np.uint8)
        img_top100 = Image.fromarray(tmp)    
        img_top100.save('temp'+str(factor)+'.png')     
        '''

    
    
    print('-----GENERATEiMAGE : generateHeidiImage ------')
    #color_palette = sns.color_palette("cubehelix", 100)
    color_palette=sns.color_palette("cubehelix", 200)
    color_palette=[(int(a*255),int(b*255),int(c*255)) for (a,b,c) in color_palette]
    
    arr=np.zeros((heidi_matrix.shape[0],heidi_matrix.shape[1],3))
    count=0
    print(bit_subspace)
    val_color_map={}
    for i in range(heidi_matrix.shape[0]):
        for j in range(heidi_matrix.shape[1]):
            if heidi_matrix[i][j] in bit_subspace.keys():
                arr[i][j]=list(wb.hex_to_rgb(bit_subspace[heidi_matrix[i][j]]))
            elif heidi_matrix[i][j] in val_color_map.keys():
                arr[i][j]=val_color_map[heidi_matrix[i][j]]
            elif(heidi_matrix[i][j]!=0):
                t=list(color_palette[0])
                #t=list(color_palette[count])
                #arr[i][j]=t
                #count+=1
                #val_color_map[heidi_matrix[i][j]]=t
                #if(count>100): break
            else:
                arr[i][j]=[255,255,255]
            #if(heidi_matrix[i][j]==0): arr[i][j]=[0,0,0]
            #else: arr[i][j]=[255,255,255] 
    tmp=arr.astype(np.uint8)
    img_top100 = Image.fromarray(tmp)  
    img_top100.save('cmp'+str(factor)+'.png')     

        #img_top100.save('temp.png')     
    
    #hh.getMappingDict(heidi_matrix,);
    return img_top100  ,heidi_matrix  
    


if __name__=='__main__':
    #iris dataset
    #datasetPath='../checking-ordering-of-points/dataset/wine/winequality-red.csv'
    #inputData=pd.read_csv(filepath_or_buffer=datasetPath,sep=';')
    '''
    outputPath='./output/wine-red/test2_orig'
    generateHeidiMatrixResults_test4(outputPath,inputData,1)
    outputPath='./output/wine-red/test2_1d'
    generateHeidiMatrixResults_kd(outputPath,inputData,1)
    outputPath='./output/wine-red/test2_2d'
    generateHeidiMatrixResults_kd(outputPath,inputData,2)
    outputPath='./output/wine-red/test2_3d'
    generateHeidiMatrixResults_kd(outputPath,inputData,3)
    '''
    datasetPath='../static/dataset/banknote_less.csv'
    outputPath='../output1'
    #datasetPath='../Data/iris.csv'
    inputData=pd.read_csv(filepath_or_buffer=datasetPath,sep=',')
    del inputData['id']
    subspaceDict={}
    #id,var_WTI,skewness_WTI,curtosis_WTI,entropy_image,classLabel
    subspaceDict['#123451']=[['var_WTI'],['var_WTI','skewness_WTI']]
    subspaceDict['#aa3351']=[['var_WTI']]
    
    #CLOSED image to composite
    color_dict,_=dbc.loadColorFromDatabase('banknote_less'+'_closed')
    temp={}
    for k in color_dict:
        temp[k.replace('H','#')]=color_dict[k]
    #print(temp)    
    img=createCompositeHeidi(inputData,temp,knn=20)
    img.save('temp.png') 
    #outputPath='../Results/iris'
    #generateHeidiMatrixResults_kd(outputPath,inputData,4)


    #outputPath='./output/data_banknote_authentication/test2_orig'
    #generateHeidiMatrixResults_test4(outputPath,inputData,1)
