import os
import shutil

import pandas as pd
import numpy as np
import math
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import operator
from mod_dim import orderPoints as op
from mod_dim import bea2
from PIL import Image
import seaborn as sns
import webcolors as wb

threshold=80

global_count=0
global_map_dict={}

def create_empty_folder(dir='output'):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)
'''
def getMappingDictForOtherSubspaces(heidi_matrix,bs,count=0,bit_map={}):

    print('-----GENERATEiMAGE : getMappingDictForOtherSubspaces ------')
    unique, counts = np.unique(heidi_matrix, return_counts=True)
    freq_dict=dict(zip(unique, counts))
    sorted_x = sorted(freq_dict.items(), key=operator.itemgetter(1),reverse=True)
    cluster_colors = sns.color_palette("hls", 100)
    map_dict={}
    print('threshold',threshold,sorted_x)
    for i,j in sorted_x:
        if(i!=0):
            if(i in bit_map.keys()):
                map_dict[i]=bit_map[i]
            else:
                map_dict[i]=cluster_colors[count]
                count+=1
                if(count>=threshold):
                    break

    img_info={}
    for k in map_dict.keys():
        t=bin(k)[2:]
        tmp=[len(t)-1-i for i, e in enumerate(t) if e != '0']
        str1=''
        for i in tmp:
            str1=str1+','+str(bs[i])
        img_info[str(tuple(map_dict[k]))]=str1[1:]
    all_info={}
    all_info['rgb_subspace']=img_info
    all_info['subspaces']=bs

    return map_dict,all_info
'''
def getMappingDictClosedImg(heidi_matrix,bs,val_map,mapping_dict,count=0):
    '''
    global global_count,global_map_dict
    print('-----GENERATEiMAGE : getMappingDictClosedImg ------')
    unique, counts = np.unique(heidi_matrix, return_counts=True)
    freq_dict=dict(zip(unique, counts))
    sorted_x = sorted(freq_dict.items(), key=operator.itemgetter(1),reverse=True)
    cluster_colors = [[51,98,107],  [240,74,28],  [219,65,226],  [72,198,33],  [96,56,90],  [62,86,23],  [112,146,236],  [241,63,122],  [190,169,39],  [118,54,14],  [217,155,187],  [71,190,192],  [227,147,102],  [118,180,101],  [159,47,132],  [216,133,224],  [107,78,181],  [174,37,43],  [73,98,152],  [232,127,43],  [194,103,105],  [97,177,216],  [170,121,34],  [163,165,86],  [56,103,72],  [54,158,43],  [86,59,28],  [224,57,163],  [177,95,231],  [232,102,155],  [95,188,156],  [156,91,152],  [117,45,66],  [114,119,28],  [161,69,179],  [69,69,86],  [167,110,81],  [150,167,219],  [131,47,44],  [62,143,155],  [128,106,143],  [234,93,83],  [230,100,220],  [191,153,224],  [195,154,89],  [99,85,21],  [228,157,51],  [169,54,77],  [73,62,122],  [193,98,71],  [115,43,104],  [131,112,234],  [125,195,50],  [188,48,20],  [222,53,85],  [168,51,109],  [99,128,154],  [134,157,43],  [46,107,25],  [226,105,185],  [70,192,134],  [174,114,139],  [134,180,193],  [75,149,213],  [70,187,98],  [232,47,190],  [236,60,58],  [34,74,67],  [158,110,200],  [232,102,119],  [59,132,121],  [66,111,214],  [78,128,73],  [233,44,138],  [128,120,61],  [149,94,36],  [166,145,190],  [96,105,180],  [88,159,115],  [50,76,111],  [218,125,167],  [238,142,139],  [186,50,166],  [94,64,146],  [169,185,45],  [155,61,26],  [115,62,44],  [69,74,32],  [200,161,68],  [209,99,43],  [151,80,97],  [95,135,50],  [105,165,49],  [237,122,97],  [37,77,33],  [161,186,94],  [64,206,71],  [122,80,102],  [202,44,105],  [115,82,40]  ];
    map_dict={}
    print('threshold',threshold,sorted_x)
    for i,j in sorted_x:
        if(i!=0):
            map_dict[i]=cluster_colors[count]
            count+=1
            if(count>=threshold):
                break

    img_info={}
    for k in map_dict.keys():
        t=bin(k)[2:]
        tmp=[len(t)-1-i for i, e in enumerate(t) if e != '0']
        str1=''
        for i in tmp:
            str1=str1+','+str(bs[i])
        img_info[str(tuple(map_dict[k]))]=str1[1:]

    all_info={}
    all_info['rgb_subspace']=img_info
    all_info['subspaces']=bs
    global_count=count
    global_map_dict.update(map_dict)
    return map_dict,all_info
    '''
    global global_count,global_map_dict
    print('-----GENERATEiMAGE : getMappingDictClosedImg ------')
    unique, counts = np.unique(heidi_matrix, return_counts=True)
    freq_dict=dict(zip(unique, counts))
    sorted_x = sorted(freq_dict.items(), key=operator.itemgetter(1),reverse=True)
    #TODO: select diff set of colors
    cluster_colors = [[51,98,107],  [240,74,28],  [219,65,226],  [72,198,33],  [96,56,90],  [62,86,23],  [112,146,236],  [241,63,122],  [190,169,39],  [118,54,14],  [217,155,187],  [71,190,192],  [227,147,102],  [118,180,101],  [159,47,132],  [216,133,224],  [107,78,181],  [174,37,43],  [73,98,152],  [232,127,43],  [194,103,105],  [97,177,216],  [170,121,34],  [163,165,86],  [56,103,72],  [54,158,43],  [86,59,28],  [224,57,163],  [177,95,231],  [232,102,155],  [95,188,156],  [156,91,152],  [117,45,66],  [114,119,28],  [161,69,179],  [69,69,86],  [167,110,81],  [150,167,219],  [131,47,44],  [62,143,155],  [128,106,143],  [234,93,83],  [230,100,220],  [191,153,224],  [195,154,89],  [99,85,21],  [228,157,51],  [169,54,77],  [73,62,122],  [193,98,71],  [115,43,104],  [131,112,234],  [125,195,50],  [188,48,20],  [222,53,85],  [168,51,109],  [99,128,154],  [134,157,43],  [46,107,25],  [226,105,185],  [70,192,134],  [174,114,139],  [134,180,193],  [75,149,213],  [70,187,98],  [232,47,190],  [236,60,58],  [34,74,67],  [158,110,200],  [232,102,119],  [59,132,121],  [66,111,214],  [78,128,73],  [233,44,138],  [128,120,61],  [149,94,36],  [166,145,190],  [96,105,180],  [88,159,115],  [50,76,111],  [218,125,167],  [238,142,139],  [186,50,166],  [94,64,146],  [169,185,45],  [155,61,26],  [115,62,44],  [69,74,32],  [200,161,68],  [209,99,43],  [151,80,97],  [95,135,50],  [105,165,49],  [237,122,97],  [37,77,33],  [161,186,94],  [64,206,71],  [122,80,102],  [202,44,105],  [115,82,40]  ];
    map_dict={}
    #mapping_dict1 = dict((tuple(v),k) for k,v in mapping_dict.iteritems()) #added -  08/august
    print('-----------------------------------------------------------------------------------------')
    print(mapping_dict.keys())
    #print(mapping_dict.keys())
    print('threshold',threshold)
    for i,j in sorted_x:
        if(i!=0):
            #print(i,)
            if i in mapping_dict:
                #print('composite legend if',i)
                map_dict[i]=mapping_dict[i]#cluster_colors[count]
            else:
                #print('composite legend else',i,mapping_dict.keys(), i in mapping_dict.keys())
                map_dict[i]=cluster_colors[count]
            count+=1
            if(count>=threshold):
                break
    img_info={}
    print(bs)
    for k in map_dict.keys():
        t=bin(k)[2:]
        tmp=[len(t)-1-i for i, e in enumerate(t) if e != '0']
        print('-llll-',t,tmp,k)
        str1=''
        for i in tmp:
            if i in bs:
                str1=str1+','+str(bs[i])
            else:
                print('ERROR',k,tmp)
        if(str1!=''):
            img_info[str(tuple(map_dict[k]))]=str1[1:]
    all_info={}
    all_info['rgb_subspace']=img_info
    all_info['subspaces']=bs
    global_count=count
    global_map_dict.update(map_dict)
    return map_dict,all_info

def getMappingDict(heidi_matrix,bs,count=0):
    global global_count,global_map_dict
    print('-----GENERATEiMAGE : getMappingDict ------')
    unique, counts = np.unique(heidi_matrix, return_counts=True)
    freq_dict=dict(zip(unique, counts))
    sorted_x = sorted(freq_dict.items(), key=operator.itemgetter(1),reverse=True)
    cluster_colors = [[51,98,107],  [240,74,28],  [219,65,226],  [72,198,33],  [96,56,90],  [62,86,23],  [112,146,236],  [241,63,122],  [190,169,39],  [118,54,14],  [217,155,187],  [71,190,192],  [227,147,102],  [118,180,101],  [159,47,132],  [216,133,224],  [107,78,181],  [174,37,43],  [73,98,152],  [232,127,43],  [194,103,105],  [97,177,216],  [170,121,34],  [163,165,86],  [56,103,72],  [54,158,43],  [86,59,28],  [224,57,163],  [177,95,231],  [232,102,155],  [95,188,156],  [156,91,152],  [117,45,66],  [114,119,28],  [161,69,179],  [69,69,86],  [167,110,81],  [150,167,219],  [131,47,44],  [62,143,155],  [128,106,143],  [234,93,83],  [230,100,220],  [191,153,224],  [195,154,89],  [99,85,21],  [228,157,51],  [169,54,77],  [73,62,122],  [193,98,71],  [115,43,104],  [131,112,234],  [125,195,50],  [188,48,20],  [222,53,85],  [168,51,109],  [99,128,154],  [134,157,43],  [46,107,25],  [226,105,185],  [70,192,134],  [174,114,139],  [134,180,193],  [75,149,213],  [70,187,98],  [232,47,190],  [236,60,58],  [34,74,67],  [158,110,200],  [232,102,119],  [59,132,121],  [66,111,214],  [78,128,73],  [233,44,138],  [128,120,61],  [149,94,36],  [166,145,190],  [96,105,180],  [88,159,115],  [50,76,111],  [218,125,167],  [238,142,139],  [186,50,166],  [94,64,146],  [169,185,45],  [155,61,26],  [115,62,44],  [69,74,32],  [200,161,68],  [209,99,43],  [151,80,97],  [95,135,50],  [105,165,49],  [237,122,97],  [37,77,33],  [161,186,94],  [64,206,71],  [122,80,102],  [202,44,105],  [115,82,40]  ];
    map_dict={}
    print('threshold',threshold)
    for i,j in sorted_x:
        if(i!=0):
            map_dict[i]=cluster_colors[count]
            count+=1
            if(count>=threshold):
                break
    print(bs)
    img_info={}
    for k in map_dict.keys():
        print(k)
        t=bin(k)[2:]
        tmp=[len(t)-1-i for i, e in enumerate(t) if e != '0']
        
        str1=''
        for i in tmp:
            if i in bs:
                print('hello')
                str1=str1+','+str(bs[i])
                img_info[str(tuple(map_dict[k]))]=str1[1:]
            else:
                print('ERROR',k,tmp)        
        

    all_info={}
    all_info['rgb_subspace']=img_info
    all_info['subspaces']=bs
    global_count=count
    global_map_dict.update(map_dict)
    return map_dict,all_info

def createBar(array):
    #CHANGE LATER FOR PAPER
    color_list = [ [255,69,0],[0,191,255],[148,0,211],[255,215,0],[65,105,225],[165,42,42],[62,86,23],[51,98,107],  [112,146,236],  [241,63,122],  [190,169,39],  [118,54,14],  [217,155,187],  [71,190,192],  [227,147,102],  [118,180,101],  [159,47,132],  [216,133,224],  [107,78,181],  [174,37,43],  [73,98,152],  [232,127,43],  [194,103,105],  [97,177,216],  [170,121,34],  [163,165,86],  [56,103,72],  [54,158,43],  [86,59,28],  [224,57,163],  [177,95,231],  [232,102,155],  [95,188,156],  [156,91,152],  [117,45,66],  [114,119,28],  [161,69,179],  [69,69,86],  [167,110,81],  [150,167,219],  [131,47,44],  [62,143,155],  [128,106,143],  [234,93,83],  [230,100,220],  [191,153,224],  [195,154,89],  [99,85,21],  [228,157,51],  [169,54,77],  [73,62,122],  [193,98,71],  [115,43,104],  [131,112,234],  [125,195,50],  [188,48,20],  [222,53,85],  [168,51,109],  [99,128,154],  [134,157,43],  [46,107,25],  [226,105,185],  [70,192,134],  [174,114,139],  [134,180,193],  [75,149,213],  [70,187,98],  [232,47,190],  [236,60,58],  [34,74,67],  [158,110,200],  [232,102,119],  [59,132,121],  [66,111,214],  [78,128,73],  [233,44,138],  [128,120,61],  [149,94,36],  [166,145,190],  [96,105,180],  [88,159,115],  [50,76,111],  [218,125,167],  [238,142,139],  [186,50,166],  [94,64,146],  [169,185,45],  [155,61,26],  [115,62,44],  [69,74,32],  [200,161,68],  [209,99,43],    [95,135,50],  [105,165,49],  [237,122,97],  [37,77,33],  [161,186,94],  [64,206,71],  [122,80,102],  [202,44,105],  [115,82,40]  ];
    #color_list = sns.color_palette("cubehelix", len(array)).as_hex()
    pos=0
    map_dict={}
    #print(set(array),array.shape)
    for i in set(array):
        map_dict[i]=color_list[pos]
        #map_dict[i]=list(wb.hex_to_rgb(color_list[pos]))
        pos+=1

    color_bar=[]
    for i in range(len(array)):
        color_bar.append(map_dict[array[i]])
    return color_bar,map_dict

def visualizeConsolidatedImage(heidi_img,algo1_bar,img_name):

    width,height=heidi_img.shape[0],heidi_img.shape[1]
    margin=int(width/4)
    img_width,img_height=(width+2*margin,height+2*margin+int(margin*1.5))
    x=np.zeros((img_width,img_height,heidi_img.shape[2]),dtype=np.uint8)

    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            x[i][j]=[0,50,0]
    for i in range(margin,width+margin):
        for j in range(margin,height+margin):
            x[i][j]=heidi_img[i-margin][j-margin]

    for i in range(0,len(algo1_bar)):
        w=int(margin/5)
        for j in range(3*w,int(3.5*w)):
            x[j][i+margin]=algo1_bar[i]

        for j in range(3*w,int(3.5*w)):
            x[i+margin][j]=algo1_bar[i]

    img = Image.fromarray(x[:,0:img_height-margin,:])
    img.save(img_name)
    return

def generateHeidiImage_hex(heidi_matrix,transform_dict):
    print('-----GENERATEiMAGE : generateHeidiImage ------')
    arr=np.zeros((heidi_matrix.shape[0],heidi_matrix.shape[1],3))
    for i in range(heidi_matrix.shape[0]):
        for j in range(heidi_matrix.shape[1]):
            if heidi_matrix[i][j] in transform_dict.keys():
                arr[i][j]=wb.hex_to_rgb(transform_dict[heidi_matrix[i][j]])
            else:
                arr[i][j]=[255,255,255]
    tmp=arr.astype(np.uint8)
    img_top100 = Image.fromarray(tmp)
    return img_top100,tmp

def generateHeidiImage(heidi_matrix,transform_dict):
    print('-----GENERATEiMAGE : generateHeidiImage ------')
    arr=np.zeros((heidi_matrix.shape[0],heidi_matrix.shape[1],3))
    for i in range(heidi_matrix.shape[0]):
        for j in range(heidi_matrix.shape[1]):
            if heidi_matrix[i][j] in transform_dict.keys():
                arr[i][j]=transform_dict[heidi_matrix[i][j]]
            else:
                arr[i][j]=[255,255,255]
    tmp=arr.astype(np.uint8)
    img_top100 = Image.fromarray(tmp)
    return img_top100,tmp

def saveHeidiImage(img,outputPath,filename):
    print('-----GENERATEiMAGE : saveHeidiImage ------')
    img.save(outputPath+'/'+filename)

def createLegend(map_dict,all_info,output_fname):
    html_str='<table border=1>\n'
    html_str+='<tr><td><b>Color</b></td><td><b>Set of subspaces</b></td><td>select</td></tr>\n'
    for val in map_dict:
        rgb=map_dict[val]
        r=rgb[0]
        g=rgb[1]
        b=rgb[2]
        if str(tuple(rgb)) in all_info['rgb_subspace']:
            html_str+=("<tr><td bgcolor=#%2x%2x%2x class='backgroundcolor'></td><td>%s</td><td><input type='checkbox' name='color' value='#%2x%2x%2x'></td></tr>" %(r,g,b,all_info['rgb_subspace'][str(tuple(rgb))],r,g,b))
        else:
            print('ERROR')
    html_str+='</table>'
    Html_file= open(output_fname,"w")
    Html_file.write(html_str)
    Html_file.close()

def dictForDatabase(map_dict,all_info):
    dict1={}
    for val in map_dict:
        rgb=map_dict[val]
        hexval='%02x%02x%02x' % tuple(rgb)
        if str(tuple(rgb)) in all_info['rgb_subspace']:
            dict1[hexval]=all_info['rgb_subspace'][str(tuple(rgb))]
    return dict1
