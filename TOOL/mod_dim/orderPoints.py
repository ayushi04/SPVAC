    # -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 08:35:24 2017

@author: Ayushi
"""
import pandas as pd
#from app.mod_visual import readDataset as rd
from scipy.spatial import distance
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree
from sklearn.neighbors import NearestNeighbors

#BFS TRAVERSAL OF KNN GRAPH
def matrix_to_list(matrix):
    graph = {}
    for i, node in enumerate(matrix):
        adj = []
        for j, connected in enumerate(node):
            if connected:
                adj.append(j)
        graph[i] = adj
    return graph

def bfs(graph, v):
    all = []
    Q = []
    Q.append(v)
    while Q != []:
        v = Q.pop(0)
        all.append(v)
        for n in graph[v]:
            if n not in Q and n not in all:
                Q.append(n)
    return all

def getKnnMatrix(data,point,knn=20):
    #print(np.zeros(data.shape[1]-2))
    knn=min(int(data.shape[0]/4),20)
    if 'id' in data.columns:
        del data['id']
    start_point=closest_node_origin(data.iloc[:,:-2].copy())
    nbrs=NearestNeighbors(n_neighbors=knn,algorithm='ball_tree').fit(data.iloc[:,:-2])
    temp=nbrs.kneighbors_graph(data.iloc[:,:-2]).toarray()
    graph=matrix_to_list(temp)
    order = bfs(graph, start_point)
    data=data.reset_index()
    data=data.reindex(order)
    data.index=data['id']
    del data['id']
    return data
    #return graph

def closest_node_origin(allData):
    allData=allData.reset_index(drop=True)
    row,col=allData.shape
    dist = np.sqrt(np.sum((allData.iloc[:,:])**2, axis=1))
    index=np.argmin(dist)
    print(index)
    return index

#HELPER METHOD FOR getConnectedDistance AND mst ORDERING
#approach2 : connected distance between points
def closest_node(allData, node):
    row,col=allData.shape
    dist = np.sqrt(np.sum((allData.iloc[:,0:col-4] - node)**2, axis=1))
    index=np.argmin(dist[~allData.loc[:,'done']])
    return index


#HELPER METHOD FOR : orderPoints_nearest_to_all
def farthest_node(allData, node):
    row,col=allData.shape
    dist = np.sqrt(np.sum((allData.iloc[:,0:col-4] - node)**2, axis=1))
    index=np.argmax(dist[~allData.loc[:,'done']])
    return index

#HELPER METHOD FOR : orderPoints_nearest_to_all
def closest_node_so_far(allData):
    row,col=allData.shape
    #done_nodes=allData[allData['done']==False].copy()
    alldist=np.zeros(allData.shape[0])
    q1=allData
    for node in range(allData.shape[0]):
        if(allData.iloc[node,-2]==True):
            ##print(node)
            dist = np.sqrt(np.sum((allData.iloc[:,0:col-4] - allData.iloc[node,0:col-4])**2, axis=1))
            alldist+=dist

    allData['dist']=alldist
    q2=allData
    #index=np.argmin(alldist[~allData.loc[:,'done']])
    index=allData[~allData.loc[:,'done']].loc[:,'dist'].idxmin()
    q1=index
    ##print(index)
    return index

def orderPoints_nearest_to_all(trainingSet,point):
    row,col=trainingSet.shape
    trainingSet['done']=False
    trainingSet['pos']=-1
    count=int(0)
    rownum=farthest_node(trainingSet.copy(),point)
    trainingSet.loc[rownum,'done']=True
    trainingSet.loc[rownum,'pos']=count
    count+=1

    while(not all(trainingSet.loc[:,'done'])):
        rownum=closest_node_so_far(trainingSet.copy())
        trainingSet.loc[rownum,'done']=True
        trainingSet.loc[rownum,'pos']=count
        count+=1
        ##print(count)
    trainingSet=trainingSet.sort_values(['pos'],ascending=['False'])
    trainingSet = trainingSet.drop('done', 1)
    trainingSet = trainingSet.drop('pos', 1)
    return trainingSet

#APPROACH 1 : CENTROID DISTANCE
#RETURN DATAFRAME allData SORTED BASED ON DISTANCE FROM CENTROID
def getDistances(allData,centroid):
    row,col=allData.shape
    allData['distance']=-1
    for i in range(row):
        dist=distance.euclidean(allData.iloc[i,0:col-2],centroid)
        allData.iloc[i,-1]=dist
    #print(allData['distance'])
    allData=allData.sort_values(['distance'],ascending=['False'])
    return allData

#APPROACH 2: CONNECTED DISTANCE
def getConnectedDistances(trainingSet,point):
    row,col=trainingSet.shape
    trainingSet['done']=False
    trainingSet['pos']=-1
    ##print(col,point,trainingSet.iloc[0,:])

    count=int(0)
    while(not all(trainingSet.loc[:,'done'])):
        rownum=closest_node(trainingSet.copy(),point)
        trainingSet.loc[rownum,'done']=True
        trainingSet.loc[rownum,'pos']=count
        count+=1
        point=trainingSet.loc[rownum,:].copy()
        point=point.iloc[0:col-2]

    trainingSet=trainingSet.sort_values(['pos'],ascending=['False'])
    ##print (trainingSet)

    #del trainingSet['done']
    #del trainingSet['pos']
    trainingSet = trainingSet.drop('done', 1)
    trainingSet = trainingSet.drop('pos', 1)

    ##print(trainingSet.iloc[0,:])
    return trainingSet

#apporach3 : minimum spanning tree
def minSpanningTree(trainingSet,testInstance):
    row,col=trainingSet.shape
    dists = distance.cdist(trainingSet.iloc[:,0:col-2],trainingSet.iloc[:,0:col-2], 'euclidean')
    mst=minimum_spanning_tree(dists)
    trainingSet['done']=False
    trainingSet['pos']=-1
    count=0
    mst=mst.toarray().astype(float)
    rownum=farthest_node(trainingSet.copy(),testInstance)
    #rownum=closest_node(trainingSet,testInstance)
    point=trainingSet.loc[rownum,:].copy()
    point=point.iloc[0:col-2]
    trainingSet.loc[rownum,'done']=True
    trainingSet.loc[rownum,'pos']=count#    distances=[]
    stack = [trainingSet.index.get_loc(rownum)] #(point,index,distance) # serial number saved
    count+=1
    while len(stack)>0:
        rownum=stack.pop()
        rownum_orig=trainingSet.index.get_values()[rownum] #index value saved in orig
        point=trainingSet.loc[rownum_orig,:].copy()
        point=point.iloc[0:col-2]

        temp=list(np.nonzero(mst[rownum]))[0]
        temp1=list(np.nonzero(mst[:,rownum]))[0]
        temp=list(temp)+list(temp1)
        for i in temp:
            k=trainingSet.index.get_values()[i]
            if trainingSet.loc[k,'done']==False:
                stack.extend([i])
                trainingSet.loc[k,'done']=True
                trainingSet.loc[k,'pos']=count#    distances=[]
                count+=1

    trainingSet=trainingSet.sort_values(['pos'],ascending=['False'])
    return trainingSet.iloc[:,0:col]

'''
def dbscanBasedordering(trainingSet,centroid):
    row,col=trainingSet.shape
    dists = distance.cdist(trainingSet.iloc[:,0:col-2],trainingSet.iloc[:,0:col-2], 'euclidean')
    
    trainingSet['done']=False
    trainingSet['pos']=-1
    count=0
    rownum=farthest_node(trainingSet.copy(),centroid)
'''

def orderDimension(feature_vector,dim,order):
    #print(dim,order,feature_vector.columns)
    feature_vector = feature_vector.sort_values(dim, ascending=order)
    return feature_vector


from sklearn.decomposition import PCA
def orderPoints_pca(feature_vector,centroid):
    '''
    pca=PCA(n_components=feature_vector.shape[1]-2)
    proj=pca.fit_transform(feature_vector.iloc[:,:-2])
    #proj=proj.transpose()
    proj=pd.DataFrame(proj)
    proj['classLabel']=feature_vector['classLabel']
    proj['classLabel_orig']=feature_vector['classLabel_orig']
    proj.columns=list(feature_vector.columns)
    return minSpanningTree(proj,centroid)
    '''
    pca=PCA(n_components=1)
    one_d_proj=pca.fit_transform(feature_vector)
    feature_vector['one_d_proj']=one_d_proj
    feature_vector=feature_vector.sort_values(['one_d_proj'],ascending=['False'])
    del feature_vector['one_d_proj']
    return feature_vector

from sklearn.manifold import TSNE
def orderPoints_tsne(feature_vector,centroid):
    tsne=TSNE(n_components=1)
    one_d_proj=tsne.fit_transform(feature_vector)
    feature_vector['one_d_proj']=one_d_proj
    feature_vector=feature_vector.sort_values(['one_d_proj'],ascending=['False'])
    del feature_vector['one_d_proj']
    return feature_vector

from sklearn import manifold
def orderPoints_mds(feature_vector,centroid):
    mds=manifold.MDS(n_components=1, max_iter=100, n_init=1)
    one_d_proj=mds.fit_transform(feature_vector)
    feature_vector['one_d_proj']=one_d_proj
    feature_vector=feature_vector.sort_values(['one_d_proj'],ascending=['False'])
    del feature_vector['one_d_proj']
    return feature_vector

def orderPoints_lle(feature_vector,centroid):
    lle=manifold.LocallyLinearEmbedding(n_components=1,eigen_solver='auto',method='standard')
    one_d_proj=lle.fit_transform(feature_vector)
    feature_vector['one_d_proj']=one_d_proj
    feature_vector=feature_vector.sort_values(['one_d_proj'],ascending=['False'])
    del feature_vector['one_d_proj']
    return feature_vector

def orderPoints_eucld(feature_vector):
    centroid=np.zeros(feature_vector.shape[1]-2)
    feature_vector=getDistances(feature_vector,centroid)
    return feature_vector

def sortbasedOnclassLabel(feature_vector,ordermeasure,param={}):
    centroids={}
    #print(ordermeasure)
    for k in set(feature_vector.classLabel):
        x=feature_vector[feature_vector.classLabel==k].mean()
        x=x[0:-2]
        centroids[k]=x.values
    sorted_data=pd.DataFrame()
    if(ordermeasure=='knn_bfs'):
        feature_vector['id'] = feature_vector.index
    for i in set(feature_vector.classLabel):
        print('--ordering : ',i)
        if(ordermeasure=='centroid_distance'):
            temp=getDistances(feature_vector[feature_vector.classLabel==i].copy(),centroids[i]).iloc[:,0:-1]
            sorted_data=pd.concat([sorted_data,temp])
        elif(ordermeasure=='knn_bfs'):
            temp=getKnnMatrix(feature_vector[feature_vector.classLabel==i].copy(),centroids[i]).iloc[:,0:-1]
            sorted_data=pd.concat([sorted_data,temp])
        elif(ordermeasure=='connected_distance'):
            temp=getConnectedDistances(feature_vector[feature_vector.classLabel==i].copy(),centroids[i])
            sorted_data=pd.concat([sorted_data,temp])
        elif(ordermeasure=='mst_distance'):
            temp=minSpanningTree(feature_vector[feature_vector.classLabel==i].copy(),centroids[i])
            sorted_data=pd.concat([sorted_data,temp])
        elif(ordermeasure=='pca_ordering'):
            temp=orderPoints_pca(feature_vector[feature_vector.classLabel==i].copy(),centroids[i])
            sorted_data=pd.concat([sorted_data,temp])
        elif(ordermeasure=='tsne_ordering'):
            temp=orderPoints_tsne(feature_vector[feature_vector.classLabel==i].copy(),centroids[i])
            sorted_data=pd.concat([sorted_data,temp])
        elif(ordermeasure=='mds_ordering'):
            temp=orderPoints_mds(feature_vector[feature_vector.classLabel==i].copy(),centroids[i])
            sorted_data=pd.concat([sorted_data,temp])
        elif(ordermeasure=='lle_ordering'):
            temp=orderPoints_lle(feature_vector[feature_vector.classLabel==i].copy(),centroids[i])
            sorted_data=pd.concat([sorted_data,temp])
        elif(ordermeasure=='nearest_to_all'):
            temp=orderPoints_nearest_to_all(feature_vector[feature_vector.classLabel==i].copy(),centroids[i])
            sorted_data=pd.concat([sorted_data,temp])
        elif(ordermeasure=='dimension'):
            print('WARNING: DIMENSION CALLED')
            temp=orderDimension(feature_vector[feature_vector.classLabel==i].copy(),param['columns'],param['order'])
            sorted_data=pd.concat([sorted_data,temp])
        elif(ordermeasure=='euclidian_distance'):
            temp=orderPoints_eucld(feature_vector[feature_vector.classLabel==i].copy())
            sorted_data=pd.concat([sorted_data,temp])
    return sorted_data

if __name__=="__main__":

    #feature_vector,classLabel_numeric,class_label_dict,fv_dict, row, col=readDataset('./static/default/blobs_4d_5c_1000/blobs_4d_5c_1000.csv','yes')
    feature_vector=pd.read_csv('/home/ayushi/Ayushi/github/visualization_projects/1-add-dim/static/dataset/usda-clean-less-classLabel.csv')
    #feature_vector.loc[:,'classLabel']=classLabel_numeric
    feature_vector.loc[:,'classLabel_orig']=feature_vector.loc[:,'classLabel']
    del feature_vector['id']
    #feature_vector=feature_vector.iloc[0:10,:]
    #print(feature_vector.iloc[:,:-2])
    #print(getKnnMatrix(feature_vector,4))
    sortbasedOnclassLabel(feature_vector,'knn_bfs')

    #param={}    
    #sorted_data=sortbasedOnclassLabel(feature_vector,'euclidian_distance',param)
    #print(sorted_data.index)
    '''
    param={}
    param['columns']=[feature_vector.columns[0]]
    param['order']=[True]

    #sorted_data=sortbasedOnclassLabel(feature_vector,'pca_ordering',param)
    sorted_data=sortbasedOnclassLabel(feature_vector,'dimension',param)

    sorted_data.to_csv(path_or_buf='/home/ayushi/Desktop/dataset/blobs_2d_4c_1000_pca_ordering.csv',  index=False)
    trainingSet=feature_vector
    point=feature_vector.iloc[0,:]
    row,col=trainingSet.shape
    trainingSet['done']=False
    trainingSet['pos']=-1
    count=0
    rownum=farthest_node(trainingSet.copy(),point)
    trainingSet.loc[rownum,'done']=True
    trainingSet.loc[rownum,'pos']=count
    count+=1
    point=trainingSet.loc[rownum,:].copy()
    point=point.iloc[0:col-2]

    while(not all(trainingSet.loc[:,'done'])):
        rownum=closest_node_so_far(trainingSet.copy())
        trainingSet.loc[rownum,'done']=True
        trainingSet.loc[rownum,'pos']=count
        count+=1

    trainingSet=trainingSet.sort_values(['pos'],ascending=['False'])
    trainingSet = trainingSet.drop('done', 1)
    trainingSet = trainingSet.drop('pos', 1)
    '''

    ##print(set(sorted_data.classLabel_orig),set(sorted_data.classLabel))
    #sorted_data=sortbasedOnclassLabel(feature_vector,'connected_distance')
