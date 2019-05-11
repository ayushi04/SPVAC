from mod_heidi import heidi_visualization
import pandas as pd
import math

class SubspaceFilter:

    def __init__(self):
        self.dataset = '' #dataframe storing the input dataset (with no classLabel column)
        self.subspace_obj = ''
        self.subspaceClique = '' #interesting subspaces obtained from CLIQUE subspace selection algorithm
        self.subspaceHeidi = '' # interesting subspaces obtained from Heidi Image (based on denseness of patterns in non diagonal block)
        self.nofdims = ''
    
    """
    This method adds new dataset
    INPUT
    ------
    dataset: dataframe 
    """
    def initialize(self, dataset):
        self.dataset = dataset
        self.nofdims = len(dataset.columns)
        self.subspace_obj = heidi_visualization.SubspaceCl()
        self.subspace_obj.initialize(dataset.columns)
    """
    ---------------
    getter methods
    ---------------
    """

    def getAllSubspace(self):
        return self.subspace_obj.getAllSubspace()

    def getSubspaceClique(self):
        return self.subspaceClique

    def getSubspaceHeidi(self):
        return self.subspaceHeidi

    """
    ---------------
    setter methods
    ---------------
    """

    """
    This method identifies all interesting subspaces obtained from CLIQUE algorithm and store in list
    e.g.,
        self.subspaceClique = [(d1,d2),(d1),(d2)]
    """
    def setSubspaceClique(self):
    
        #TODO : write code here to call clique algorithm and identify interesting subspaces
        self.subspaceClique = []


    """
    This method identifies all interesting subspaces identified using denseness of patterns
    in non diagonal blocks (HEIDI based algorithm)
    e.g.,
        self.subspaceHeidi = [(d1,d2),(d1),(d2)]
    """
    def setSubspaceHeidi(self):

        #TODO: write code here to call Heidi based algorithm to identify interesting patterns
        self.subspaceHeidi = []

    



