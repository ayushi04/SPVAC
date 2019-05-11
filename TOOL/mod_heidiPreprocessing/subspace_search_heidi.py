from mod_heidi import heidi_visualization 

class SubspaceSearch_Heidi:

	def __init__(self):
		self.heidiObj = heidi_visualization.HeidiMatrix()
		self.classDistribution = [] #order of class Label is same as the one in Heidi image
		self.subspaceHeidi_map = {}
		self.sortedSubspaces = []

	def initialize(self,dataset, classDistribution):
		self.dataset = dataset
		self.classDistribution = classDistribution
		self.heidiObj.initialize(dataset)
		self.subspaceHeidi_map = self.heidiObj.getSubspaceHeidi_map()
		
	def _setDiagonalBlocks_zero(self):
		#TODO: write code here to set diagonal blocks to zero
		pass

	def _sortSubspaces_interesting(self):
		#TODO: write code here to sort subspaces based on interestingness
		pass

	def getTopAInterestingSubspace(self):
		#TODO: write code to return top A interesting subspaces
		pass




	
