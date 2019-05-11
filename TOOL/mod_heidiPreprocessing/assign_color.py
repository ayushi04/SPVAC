import webcolors as wb
import models
from app import db

class ColorAssign:

	def __init__(self):
		self.columns  = []
		self.sortedSubspaces = [] #e.g., [(d1,d2), (d1), (d2)]
		self.colorList = [ [51,98,107],  [240,74,28],  [219,65,226],  [72,198,33],  [96,56,90],  [62,86,23],  [112,146,236],  [241,63,122],  [190,169,39],  [118,54,14],  [217,155,187],  [71,190,192],  [227,147,102],  [118,180,101],  [159,47,132],  [216,133,224],  [107,78,181],  [174,37,43],  [73,98,152],  [232,127,43],  [194,103,105],  [97,177,216],  [170,121,34],  [163,165,86],  [56,103,72],  [54,158,43],  [86,59,28],  [224,57,163],  [177,95,231],  [232,102,155],  [95,188,156],  [156,91,152],  [117,45,66],  [114,119,28],  [161,69,179],  [69,69,86],  [167,110,81],  [150,167,219],  [131,47,44],  [62,143,155],  [128,106,143],  [234,93,83],  [230,100,220],  [191,153,224],  [195,154,89],  [99,85,21],  [228,157,51],  [169,54,77],  [73,62,122],  [193,98,71],  [115,43,104],  [131,112,234],  [125,195,50],  [188,48,20],  [222,53,85],  [168,51,109],  [99,128,154],  [134,157,43],  [46,107,25],  [226,105,185],  [70,192,134],  [174,114,139],  [134,180,193],  [75,149,213],  [70,187,98],  [232,47,190],  [236,60,58],  [34,74,67],  [158,110,200],  [232,102,119],  [59,132,121],  [66,111,214],  [78,128,73],  [233,44,138],  [128,120,61],  [149,94,36],  [166,145,190],  [96,105,180],  [88,159,115],  [50,76,111],  [218,125,167],  [238,142,139],  [186,50,166],  [94,64,146],  [169,185,45],  [155,61,26],  [115,62,44],  [69,74,32],  [200,161,68],  [209,99,43],  [151,80,97],  [95,135,50],  [105,165,49],  [237,122,97],  [37,77,33],  [161,186,94],  [64,206,71],  [122,80,102],  [202,44,105],  [115,82,40]  ]
		self.colormap = {}

	def initialize(self, columns, sortedSubspaces):
		self.columns = columns
		self.sortedSubspaces = sortedSubspaces
		self._setColormap()

	def _setColormap(self):
		total = min(len(self.sortedSubspaces), 100)
		for i in range(0,total):
			self.colormap[self.sortedSubspaces[i]] = wb.rgb_to_hex(self.colorList[i])
		
	def getColormap(self):
		return self.colormap


def saveColormap_DB(color_map, datasetname):
	"""
	INPUT
	------
	colormap : dictionary type
	e.g., 
	{(d1,d2):#ffff12, (d1):#ff12ff, (d2):#1234ff}
	"""
	objects = []
	for key in color_map:
		obj = models.SubspaceColorMap(datasetname, color_map[key], str(key)) #(datasetname, color, str(subspace))
		objects.append(obj)
	print(objects)
	db.session.bulk_save_objects(objects)
	db.session.commit()

def hex_to_rgb(hexColor):
	color_val = wb.hex_to_rgb(hexColor)
	rgb = tuple([color_val.red, color_val.green, color_val.blue])
	return rgb