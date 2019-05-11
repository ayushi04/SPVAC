import math
import numpy as np
import pandas as pd
import _pickle as cPickle
from sklearn.neighbors import NearestNeighbors
from PIL import Image

import models
from mod_heidiPreprocessing import assign_color
from app import db
import cv2

class SubspaceCl:

    def __init__(self):
        self.columns = []
        self.allSubspace = []
        self.nofdims = ''

    def initialize(self, columns):
        self.columns = columns
        self.nofdims = len(columns)
        self._setAllSubspace()

    """
    This method identifies all possible subspaces and saves in class variable allSubspaces
    e.g.,
        self.allSubspace = [(d1,d2),(d1),(d2)]
    """
    def _setAllSubspace(self):
        self.allSubpace = []
        
        max_count=int(math.pow(2,self.nofdims))
        allsubspaces=range(1,max_count)
        f=lambda a:sorted(a,key=lambda x:sum(int(d)for d in bin(x)[2:]))
        allsubspaces=f(allsubspaces)

        frmt=str(self.nofdims)+'b'
        for i in allsubspaces:
            bin_value=str(format(i,frmt))
            bin_value=bin_value[::-1]
            subspace_col=[self.columns[index] for index,value in enumerate(bin_value) if value=='1']
            self.allSubspace.append(tuple(subspace_col))
        return      

    def getAllSubspace(self):
        return self.allSubspace


class HeidiMatrix:

    def __init__(self):
        self.dataset = ''
        self.pointsOrder = []
        self.subspaceHeidi_map = {}
        self.subspace_obj = ''
        self.knn = 20
        self.datasetname = ''

    def initialize(self, dataset, datasetname):
        self.dataset = dataset
        self.pointsOrder = list(dataset.index)
        self.datasetname = datasetname
        self.subspace_obj = SubspaceCl()
        self.subspace_obj.initialize(dataset.columns)
        self._setSubspaceHeidi_map()
    
    def getSubspaceHeidi_map(self):
        return self.subspaceHeidi_map

    def getSubspace_obj(self):
        return self.subspace_obj
    
    def getHeidiMatrix_oneSubspace(self,subspace):
        return self.subspaceHeidi_map[subspace]

    def getHeidiMatrix(self, subspaceVector):
        #TODO : write code here to create matrix for input subspaces
        pass
    
    def getHeidiMatrix_allSubspace(self):
        #TODO : write code to create Heidi matrix for all subspaces
        pass

    def _setSubspaceHeidi_map(self):
        """
        sets the subspaceHeidi_map dictionary object
        e.g.,
        subspaceHeidi_map][tuple]=np.array([[],.....[]]) 
        subspaceHeidi_map][(d1,d2)]=np.array([[],.....[]]) 
        subspaceHeidi_map][(d1)]=np.array([[],.....[]]) 
        """
        for subspace in self.subspace_obj.getAllSubspace():
            self.subspaceHeidi_map[subspace] = self._createHeidiMatrix(subspace)

    def setSubspace_obj(self, sobj):
        self.subspace_obj = sobj

    def setSubspace_obj(self):
        self.subspace_obj = SubspaceCl
        self.subspace_obj.initialize(self.dataset.columns)

    def _createHeidiMatrix(self, subspace):
        #DONE : write Heidi algorithm to return knn matrix for this subspace
        row=self.dataset.shape[0]
        heidi_matrix=np.zeros(shape=(row,row),dtype=np.uint64)
        #subspace_col = [i for i,x in enumerate(subspace) if x]
        #filtered_data=self.inputData.iloc[:,subspace_col]
        filtered_data=self.dataset.loc[:,subspace]
        np_subspace=filtered_data.values
        nbrs=NearestNeighbors(n_neighbors=self.knn,algorithm='ball_tree').fit(np_subspace)
        temp=nbrs.kneighbors_graph(np_subspace).toarray()
        heidiMatrix=temp.astype(np.uint64)
        return heidiMatrix


class HeidiImage:

    def __init__(self):
        self.heidiMatrix_obj = HeidiMatrix()
        self.dataset = ''
        self.colorAssign = ''
        self.heidiImage = ''
        self.subspaceVector = []
        self.datasetname = ''
        self.subspaceHeidiImage_map = {}


    def initialize(self, dataset, datasetname):
        self.dataset = dataset
        self.datasetname = datasetname
        #self.heidiMatrix_obj.initialize(self.dataset, self.datasetname)
        self.colorAssign = assign_color.ColorAssign()

    def setHeidiMatrix_obj(self, hobj):
        self.heidiMatrix_obj = hobj

    def getHeidiMatrix_obj(self):
        return self.heidiMatrix_obj

    def setSubspaceVector(self, subspaceVector):
        self.subspaceVector = subspaceVector

    def getSubspaceVector(self):
        return  self.subspaceVector

    def _imageUnion(self,img1, img2):
        row = img1.shape[0]
        col = img1.shape[1]
        #print(row,col)
        for i in range(0,row):
            for j in range(0,col):
                #print(img2[i][j], type(img2[i][j]))
                if(list(img2[i][j])==[255,255,255]):
                    continue
                if(list(img1[j][j])==[255,255,255]):
                    img1[i][j]=img2[i][j]
                    continue
                img1[i][j] = (img1[i][j]+img2[i][j])/2
        return img1


    def getHeidiImage(self):
        #TODO: write code to generate composite image  
        composite_img = 0
        mask_sum=0
        for subspace in self.subspaceVector[0:]:
            heidi_matrix = self.heidiMatrix_obj.getHeidiMatrix_oneSubspace(subspace)
            mask = np.dstack((heidi_matrix, heidi_matrix, heidi_matrix))
            mask_sum +=mask
            composite_img = composite_img + np.multiply(mask, self.subspaceHeidiImage_map[subspace])

        composite_img = composite_img / mask_sum
        composite_img = composite_img.astype(np.uint8)
        index_list = np.where(np.all(composite_img == [0,0,0], axis=-1))
        composite_img[index_list]=[255,255,255]
        composite_img = Image.fromarray(composite_img)
        composite_img.save('./imgs/composite_img.png')
        return composite_img
        
    def getSubspaceHeidiImage_map(self):
        return self.subspaceHeidiImage_map

    def setSubspaceHeidiImage_map(self):
        c=1
        for subspace in self.subspaceVector:
            self.subspaceHeidiImage_map[subspace] = self.getHeidiImage_oneSubspace(subspace)
            img = Image.fromarray(self.subspaceHeidiImage_map[subspace])
            img.save('./imgs/img'+str(c)+'.png')
            c=c+1
        return

    def getHeidiImage_oneSubspace(self,subspace):
        color = models.SubspaceColorMap.query.filter_by(dataset=self.datasetname, subspace=str(subspace))
        color = assign_color.hex_to_rgb(color[0].color)
        heidi_matrix = self.heidiMatrix_obj.getHeidiMatrix_oneSubspace(subspace)
        arr = np.zeros((heidi_matrix.shape[0],heidi_matrix.shape[1],3))
        for i in range(heidi_matrix.shape[0]):
            for j in range(heidi_matrix.shape[1]):
                if(heidi_matrix[i][j]==1):
                    arr[i][j]=color
                else:
                    arr[i][j]=[255,255,255]
        tmp = arr.astype(np.uint8)
        return tmp
        #img = Image.fromarray(tmp)
        #return img


def saveHeidiMatrix_DB(subspaceHeidiMatrix_map, subspaceHeidiImage_map, datasetname):
    """
    INPUT
    ------
    subspaceHeidiMatrix_map : dictionary type
    {(d1,d2):[[0,1,.....1],.....[1,1,.......0]}
    """
    objects = []
    for key in subspaceHeidiMatrix_map:
        serialized_matrix = cPickle.dumps(subspaceHeidiMatrix_map[key])
        img = subspaceHeidiImage_map[key]
        img = Image.fromarray(img)
        serialized_image = cPickle.dumps(img)
        obj = models.SubspaceHeidiMap(str(key), datasetname, serialized_matrix, serialized_image) # (subspace:tuple_string,datasetname:string, heidi_matrix (2-d numpy array), heidi_image)
        objects.append(obj)
    db.session.bulk_save_objects(objects)
    db.session.commit()





