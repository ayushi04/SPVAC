from mod_heidiPreprocessing import assign_color, order_points, subspace_filter
from mod_heidi import heidi_visualization
from flask import session
import _pickle as cPickle

class HeidiParam:

	def __init__(self):
		self.datasetPath=''
		self.allDims = ''
		self.orderDims = ''
		self.otherDims = ''
		self.allSubspaces = ''
		self.selectedSubspace = ''
		self.allSubspaces_colormap = ''

	def __str__(self):
		string = "datasetPath:%s, allDims:%s, orderDims:%s, otherDims:%s, allSubspaces: %s" \
				"selectedSubspace:%s, allSubspaces_colormap:%s " %(self.datasetPath, self.allDims, self.orderDims, self.otherDims,\
					self.allSubspaces, self.selectedSubspace, self.allSubspaces_colormap)
		return string

	#def getCompositeImage(self):



def getAllSubspaces(dataset, datasetname):
	subspace_obj = heidi_visualization.SubspaceCl()
	subspace_obj.initialize(list(dataset.columns))
	allSubspaces = subspace_obj.getAllSubspace()
	
	colorAssign_obj = assign_color.ColorAssign()
	colorAssign_obj.initialize(dataset, allSubspaces)
	colormap = colorAssign_obj.getColormap()
	assign_color.saveColormap_DB(colormap, datasetname)

	heidiMatrix_obj = heidi_visualization.HeidiMatrix()
	heidiMatrix_obj.initialize(dataset, datasetname)
	subspaceHeidiMatrix_map = heidiMatrix_obj.getSubspaceHeidi_map()
	
	heidiImage_obj = heidi_visualization.HeidiImage()
	heidiImage_obj.initialize(dataset, datasetname)
	heidiImage_obj.setHeidiMatrix_obj(heidiMatrix_obj)
	heidiImage_obj.setSubspaceVector(allSubspaces)
	heidiImage_obj.setSubspaceHeidiImage_map()
	
	compositeImage = heidiImage_obj.getHeidiImage()
	

	subspaceHeidiImg_map = heidiImage_obj.getSubspaceHeidiImage_map()

	heidi_visualization.saveHeidiMatrix_DB(subspaceHeidiMatrix_map,subspaceHeidiImg_map,datasetname)

	paramobj = HeidiParam()
	paramobj.datasetPath = datasetname
	paramobj.allDims = list(dataset.columns)
	paramobj.allSubspaces = allSubspaces
	paramobj.allSubspaces_colormap = {str(k):colormap[k] for k in colormap}

	return paramobj, heidiImage_obj, heidiMatrix_obj