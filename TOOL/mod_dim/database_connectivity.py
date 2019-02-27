from PIL import Image,ImageDraw
from numpy import *
from mod_dim import region_label as rg
import pandas as pd
import ast
#from py2neo.packages.httpstream import http
#http.socket_timeout = 9999
# PRE-ORDER TRAVERSAL OF QUAD-TREE
def preorder(start):
    if(start==None): return
    #print(start.pixel)
    preorder(start.left)
    preorder(start.mid1)
    preorder(start.mid2)
    preorder(start.right)

# RETURNS TOTAL NUMBER OF NODES IN QUADTREE
def countNode(start):
    if(start==None): return 0;
    return countNode(start.left)+1+countNode(start.mid1)+countNode(start.mid2) +countNode(start.right)

class Point(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"

class Pixel(object):
    def __init__(self,color=[(0,0,0)],topLeft=Point(0,0),bottomRight=Point(0,0),image=None):
        self.color=color
        #self.image=image
        self.topLeft=topLeft
        self.bottomRight=bottomRight
    def getColor(self):
        return self.color[0]
    def getRowImgPoints(self):
        return list(range(self.topLeft.x,self.bottomRight.x+1))
    def getColImgPoints(self):
        return list(range(self.topLeft.y,self.bottomRight.y+1))
    def __str__(self):
        return "Pixel:" + str(self.color) + "coordinates : " + str(self.topLeft) + ":" + str(self.bottomRight)

#def quadTree(image,pixel):
class quadTree(object):
    def __init__(self, image,tl,br):
        self.pixel = imageInfo(image,tl,br) #colorlist,top-left-pixel-coordinates, bottom-right-pixel-coordinates
        self.left = None
        self.mid1 = None
        self.mid2 = None
        self.right = None

def getCoordinates(pixels,sortedPath,unique=True):
    rowPointsIndex=[]
    colPointsIndex=[]
    pair=[]
    x=pd.read_csv(sortedPath,index_col=0)
    for p in pixels:
        tl=p.topLeft
        br=p.bottomRight
        for i in range(tl.x,br.x+1):
            for j in range(tl.y,br.y+1):
                rowPointsIndex.extend([i])
                colPointsIndex.extend([j])
                #pair.extend([str(i)+':'+str(j)])
                pair.extend([x.index.get_values()[i]+':'+x.index.get_values()[j]])
        #print(rowPointsIndex,colPointsIndex,tl,br)
    if(unique==True):
        rowPointsIndex=list(set(rowPointsIndex))
        colPointsIndex=list(set(colPointsIndex))
    print('---',len(rowPointsIndex),len(colPointsIndex))
    rowPoints = x.iloc[rowPointsIndex,:]
    colPoints = x.iloc[colPointsIndex,:]
    return rowPoints,colPoints,pair

# GIVEN IMAGE, TL AND BR IT RETURN PIXEL OBJECT CONTAINING TL, BL AND COLORLIST IN HEX
def imageInfo(image,tl,br):
    t=image.crop((tl.x,tl.y,br.x+1,br.y+1))
    t=t.convert('RGB')
    color_list=t.getcolors(maxcolors=10000)
    #color_list=image.crop((tl.x,tl.y,br.x+1,br.y+1)).getcolors(maxcolors=200)
    #print(color_list)
    color_list=[b for (a,b) in color_list]
    color_list=['#%02x%02x%02x' % (r,g,b) for (r,g,b) in color_list]
    p = Pixel(color_list,tl,br)#,image)
    return p

# RETURN TRUE IF INPUT PIXELS/RECTANGLES CONTAINS ONLY ONE COLOR
def isHomogeneous(pixel):
    #print(pixel,len(pixel.color))
    if(len(pixel.color)==1): return True
    return False

# SPLIT THE BLOCK/RECTANGLE/PIXEL IN 3 QUADS RECURSIVELY
def splitBlock(node,image):
    tl=node.pixel.topLeft
    br=node.pixel.bottomRight
    if (tl.x==br.x and tl.y==br.y):
        node.left=None
        node.mid1=None
        node.mid2=None
        node.right=None
    elif((tl.x+1)==br.x and (tl.y+1)==br.y) :
        node.left=quadTree(image,tl,tl)
        node.mid1=quadTree(image,Point(tl.x,tl.y+1),Point(tl.x,tl.y+1))
        node.mid2=quadTree(image,Point(tl.x+1,tl.y),Point(tl.x+1,tl.y))
        node.right=quadTree(image,br,br)
    elif((tl.x+1)==br.x and (tl.y)==br.y) or ((tl.x)==br.x and (tl.y+1)==br.y) :
        node.left=quadTree(image,tl,tl)
        node.mid1=None
        node.mid2=None
        node.right=quadTree(image,br,br)
    else:
        xmid=int((tl.x+br.x)/2)
        ymid=int((tl.y+br.y)/2)
        mid=Point(xmid,ymid)
        node.left=quadTree(image,tl,Point(xmid,ymid))
        node.mid1=quadTree(image,Point(tl.x,ymid+1),Point(xmid,br.y))
        node.mid2=quadTree(image,Point(xmid+1,tl.y),Point(br.x,ymid))
        node.right=quadTree(image,Point(xmid+1,ymid+1),br)
    if node.left!=None:
        if not isHomogeneous(node.left.pixel): splitBlock(node.left,image)
    if node.mid1!=None:
        if not isHomogeneous(node.mid1.pixel): splitBlock(node.mid1,image)
    if node.mid2!=None:
        if not isHomogeneous(node.mid2.pixel): splitBlock(node.mid2,image)
    if node.right!=None:
        if not isHomogeneous(node.right.pixel): splitBlock(node.right,image)

# RETURNS LEAF NODES OF QUADTREE
def get_leaf_nodes(node, max_depth=None):
    if node==None:
        return []
    if node.left==None and node.mid1==None and node.mid2==None and node.right==None :
        return [node.pixel]
    result = []
    result.extend(get_leaf_nodes(node.left))
    result.extend(get_leaf_nodes(node.mid1))
    result.extend(get_leaf_nodes(node.mid2))
    result.extend(get_leaf_nodes(node.right))
    return result

# DELETE ALL NODE FROM DATABASE
def deleteAllNodes(labelname=''):
    print(labelname,'labelname')
    from py2neo import Graph, Path,authenticate
    authenticate("localhost:7474", "neo4j", "japan123")
    graph = Graph()
    if(labelname!=''):
        tx = graph.cypher.execute('MATCH (n) where n.name={x} DELETE n',x=labelname)
    else:
        tx = graph.cypher.execute('MATCH (n) DELETE n')

# SAVE COLOR DICTIONARY TO DATABASE
def saveColorToDatabase(colorDict,datasetname):
    #write code here to save to database
    print('---SAVING COLOR DICT IN DATABASE----')
    from py2neo import Graph, Path,authenticate,Node,Relationship
    authenticate("localhost:7474", "neo4j", "japan123")
    tx = Graph()
    tx.cypher.execute('MATCH (n:color) where n.name={x} DELETE n',x=datasetname)
    u1=Node('color',name=datasetname)
    tx.create(u1)
    for k in colorDict.keys():
        u1.properties['H'+k] = str(colorDict[k])
        u1.push()

    #print(' -- successfully saved color dictionary in database!')

# LOAD LEGEND FROM DATABASE AS DICTIONARY and SET OF ALL SUBSPACES IN IMAGE
def loadColorFromDatabase(datasetname):
    print('--LOADING COLORDICT FROM DATABASE')
    from py2neo import  Graph,Path,authenticate,Node,Relationship
    authenticate("localhost:7474","neo4j","japan123")
    tx=Graph()
    opt=tx.cypher.execute('MATCH (n:color) where n.name={x} return keys(n)', x=datasetname)
    allColors=str(opt).split('[')[1].split(']')[0]
    allColors=allColors.replace('\'','')
    allColors=allColors.replace(' ','')
    allColors=allColors.replace('uH','H') #python2
    allColors=allColors.replace('uname','name') #python2
    allColors=allColors.split(',')
    allColors.remove('name')
    #print('allColors in database are:',allColors)
    allSubspace=set([])
    color_dict={}
    for a in allColors:
        str1='MATCH (n:color) where n.name=\'%s\' return n.%s' %(datasetname,a)
        subspace=tx.cypher.execute(str1)
        n='n.'+a
        subspace='['+subspace[0][n]+']'
        subspace=ast.literal_eval(subspace)
        color_dict[a]=subspace
        for i in subspace:
            #print(i)
            allSubspace.add(tuple(i))
    subspaceList=[]
    for i in allSubspace:
        subspaceList.append(list(i))
    return color_dict,subspaceList

#RETURNS SUBSPACE GIVEN COLOR AS INPUT using database
def getColorSubspace(color,datasetName):
    print('-- getColorSubspace --',color,datasetName)
    from py2neo import Graph, Path,authenticate,Node,Relationship
    authenticate("localhost:7474", "neo4j", "japan123")
    tx = Graph()
    color = ast.literal_eval(color)[0]
    print(color[1:])
    str1='MATCH (n:color) where n.name=\'%s\' return n.%s' %(datasetName,'H'+color[1:])
    subspace=tx.cypher.execute(str1)
    subspace=subspace[0]['n.H'+color[1:]]
    return ast.literal_eval(subspace)

#RETURNS COLOR_LIST GIVEN SUBSPACE AS INPUT using database
def getColorFromSubspace(subspace,datasetName):
    from py2neo import Graph, Path,authenticate,Node,Relationship
    authenticate("localhost:7474", "neo4j", "japan123")
    tx = Graph()
    opt=tx.cypher.execute('MATCH (n:color) where n.name={x} return keys(n)', x=datasetname)
    allColors=str(opt).split('[')[1].split(']')[0]
    allColors=allColors.replace('\'','')
    allColors=allColors.replace(' ','')
    allColors=allColors.split(',')
    allColors.remove('name')


#returns row_block and col_block id's as list from database
def getAllBlock(datasetName):
    from py2neo import Graph, Path,authenticate,Node,Relationship
    authenticate("localhost:7474", "neo4j", "japan123")
    tx = Graph()
    tx = tx.cypher.execute('MATCH (n:n1) where n.name={x} RETURN n.class_count',x=datasetName)
    print(tx[0])
    class_count='['+str(tx[0]['n.class_count'])+']'
    class_count=ast.literal_eval(class_count)
    block_row=[i for i in range(len(class_count))]
    block_col=[i for i in range(len(class_count))]
    return block_row,block_col

#returns patterns for given color,blockid, dataset
#INPUT e.g., iris.csv,int(0),int(1),str('[\''+'#122547'+'\']')
def getBlockPatternsColor(datasetName,block_row,block_col,color_val='ALL',imgType=''): #eg. iris.csv
    print('-- blockfilter: retrieving pixels associated with the clicked pattern ')
    from py2neo import Graph, Path,authenticate
    authenticate("localhost:7474", "neo4j", "japan123")
    graph = Graph()
    labelname=datasetName.split('.')[0]+imgType
    if(color_val=='ALL'):
        tx = graph.cypher.execute('match (n) WHERE EXISTS(n.color) and n.name={lb} and toFloat(n.block_row)={x} and toFloat(n.block_col)={y}  RETURN n.brx, n.bry,n.lbl,n.tlx,n.tly,n.color',lb=labelname,x=block_row,y=block_col)    
    else:
        tx = graph.cypher.execute('match (n) WHERE EXISTS(n.color) and n.name={lb} and toFloat(n.block_row)={x} and toFloat(n.block_col)={y} and n.color={c}  RETURN n.brx, n.bry,n.lbl,n.tlx,n.tly,n.color',lb=labelname,x=block_row,y=block_col,c=color_val)
    pixels=[]
    for i in tx:
        tl=[int(i['n.tlx']),int(i['n.tly'])]
        br=[int(i['n.brx']),int(i['n.bry'])]
        color = i['n.color']
        p=Pixel(ast.literal_eval(color),Point(tl[0],tl[1]),Point(br[0],br[1]))
        pixels.extend([p])
    #for i in pixels:
    #    print(str(i))
    print('\t 1. Total pixels in the selected pattern is %d' %(len(pixels)))
    return pixels


# SAVE ONLY THE LEAF NODES OF QUAD TREE IN DATABASE
def saveMatrixToDatabase_leaf_v2(image,bit_subspace,outputPath,sorted_data,lbl,labelname='n1'):
    #write code here to save to database
    print('---CREATING QUADTREE FOR IMAGE----')
    q=quadTree(image,Point(0,0),Point(image.size[0]-1,image.size[1]-1))
    splitBlock(q,image)
    from py2neo import Graph, Path,authenticate,Node,Relationship
    authenticate("localhost:7474", "neo4j", "japan123")
    graph = Graph("http://localhost:7474/db/data/")
    queries=[]
    def preorder1(start):
        if(start==None): return
        #print(start.pixel)
        if((len(start.pixel.color)==1) and (sorted_data.iloc[int(start.pixel.topLeft.x),-1] == sorted_data.iloc[int(start.pixel.bottomRight.x),-1]) and ( sorted_data.iloc[int(start.pixel.topLeft.y),-1] == sorted_data.iloc[int(start.pixel.bottomRight.y),-1] )):
            #u1=Node(labelname,name=labelname,tlx=str(start.pixel.topLeft.x),tly=str(start.pixel.topLeft.y),brx=str(start.pixel.bottomRight.x),bry=str(start.pixel.bottomRight.y),color=str(start.pixel.color),lbl=lbl[start.pixel.topLeft.y][start.pixel.topLeft.x])
            tlx=str(start.pixel.topLeft.x)
            tly=str(start.pixel.topLeft.y)
            brx=str(start.pixel.bottomRight.x)
            bry=str(start.pixel.bottomRight.y)
            color=str(start.pixel.color)
            lbl1=lbl[start.pixel.topLeft.y][start.pixel.topLeft.x]
            #blockid1=blockid[start.pixel.topLeft.y][start.pixel.topLeft.x]
            block_row = sorted_data.iloc[int(tlx),-1]
            block_col = sorted_data.iloc[int(tly),-1]
            #if(sorted_data.iloc[int(tlx),-1] != sorted_data.iloc[int(brx),-1]):
            #    print('ERROR: need to divide matrix blockwise')
            #elif(sorted_data.iloc[int(tly),-1] != sorted_data.iloc[int(bry),-1]):
            #    print('ERROR: need to divide matrix blockwise')

            queries.append([labelname,tlx,tly,brx,bry,color,lbl1,block_row,block_col])

            #queries.append([labelname,tlx,tly,brx,bry,color,lbl1])
            temp=lbl[start.pixel.topLeft.y:start.pixel.bottomRight.y,start.pixel.topLeft.x:start.pixel.bottomRight.x]  #warning : temporarily resolved recheck once
            #temp=lbl[start.pixel.topLeft.y:start.pixel.bottomRight.y+1,start.pixel.topLeft.x:start.pixel.bottomRight.x+1]  #warning : temporarily resolved recheck once

            x=unique(temp)
            #if(len(x)>1 ):
            #    print("ERROR:",start.pixel,x)
            #tx.create(u1)

        preorder1(start.left)
        preorder1(start.mid1)
        preorder1(start.mid2)
        preorder1(start.right)
    #n = db.labels.create("tmp2")
    print('----SAVING QUADTREE IN DATABASE---')
    preorder1(q)
    #x=pd.DataFrame(columns=['name','tlx','tly','brx','bry','color','lbl'])
    fname='temp.csv'
    x=pd.DataFrame(queries)
    queries=pd.DataFrame(queries)
    #prev=0
    #for i in range(100000:queries.shape[0]:100000):
    t=int(queries.shape[0]/2)
    queries.iloc[0:t].to_csv('/var/lib/neo4j/import/'+fname,index=False,header=None)
    tx = graph.cypher.execute('LOAD CSV FROM \'file:///temp.csv\' AS line CREATE (:t1 { name: line[0], tlx: toInteger(line[1]), tly: toInteger(line[2]), brx: toInteger(line[3]), bry: toInteger(line[4]), color: line[5], lbl: toInteger(line[6]), block_row: toInteger(line[7]), block_col:toInteger(line[8])  })')
    queries.iloc[t:].to_csv('/var/lib/neo4j/import/'+fname,index=False,header=None)
    tx = graph.cypher.execute('LOAD CSV FROM \'file:///temp.csv\' AS line CREATE (:t1 { name: line[0], tlx: toInteger(line[1]), tly: toInteger(line[2]), brx: toInteger(line[3]), bry: toInteger(line[4]), color: line[5], lbl: toInteger(line[6]), block_row: toInteger(line[7]), block_col:toInteger(line[8])  })')
    #prev=i
        
# FETCH ONLY THOSE NODES WITH THE GIVEN COLOR IN DATABASE
def databasefilter(labelname,color='ALL'):
    print('--Database filter ALL/color--')
    from py2neo import Graph, Path,authenticate
    authenticate("localhost:7474", "neo4j", "japan123")
    graph = Graph()
    print(color)
    if(color!='ALL'):
        color='[\''+color+'\']'
        print('databasefilter : color',color)
        tx = graph.cypher.execute('match (n) WHERE EXISTS(n.color) and n.name={x} and n.color={c} RETURN n.color,n.block_col,n.block_row,n.tlx,n.tly,n.brx,n.bry',c=color,x=labelname)
    else:
        tx = graph.cypher.execute('match (n) WHERE EXISTS(n.color) and n.name={x} RETURN n.color,n.block_col,n.block_row,n.tlx,n.tly,n.brx,n.bry',x=labelname)
    pixels=[]
    for i in tx:
        color=i['n.color']
        tl = Point(int(i['n.tlx']),int(i['n.tly']))
        br = Point(int(i['n.brx']),int(i['n.bry']))
        p=Pixel(ast.literal_eval(color),tl,br)
        pixels.extend([p])
    print('/t 1. retrieved all pixels. Total count is %d' %(len(pixels)))
    return pixels

def blockfilter_composite(x,y,labelname,imgType):
    print('-- blockfilter_composite: retrieving pixels associated with the clicked pattern ')
    from py2neo import Graph, Path,authenticate
    authenticate("localhost:7474", "neo4j", "japan123")
    graph = Graph()
    t=x
    x=y
    y=t
    tx = graph.cypher.execute('match (n) WHERE EXISTS(n.color) and n.name={lb} and toFloat(n.tlx)<={x} and toFloat(n.brx)>={x} and toFloat(n.tly)<={y} and toFloat(n.bry)>={y} RETURN n.block_row,n.block_col,n.color',x=x,y=y,lb=labelname+imgType)
    print(tx[0],'block')
    color_val = tx[0]['n.color']
    block_row = tx[0]['n.block_row']
    block_col = tx[0]['n.block_col']
    tx = graph.cypher.execute('match (n) WHERE EXISTS(n.color) and n.name={lb} and toFloat(n.block_row)={x} and toFloat(n.block_col)={y} and n.color={c}  RETURN n.brx, n.bry,n.lbl,n.tlx,n.tly,n.color',lb=labelname+'_composite',x=block_row,y=block_col,c=color_val)
    pixels=[]
    for i in tx:
        tl=[int(i['n.tlx']),int(i['n.tly'])]
        br=[int(i['n.brx']),int(i['n.bry'])]
        color = i['n.color']
        p=Pixel(ast.literal_eval(color),Point(tl[0],tl[1]),Point(br[0],br[1]))
        pixels.extend([p])
    #for i in pixels:
    #    print(str(i))
    print('\t 1. Total pixels in the selected pattern is %d' %(len(pixels)))
    return pixels

def getTopLeftCoordinates_Grid(x,y,labelname,imgType):
    print('-- getTopLeftCoordinates_Grid: retrieving top left coordinates of grid ')
    from py2neo import Graph, Path,authenticate
    authenticate("localhost:7474", "neo4j", "japan123")
    graph = Graph()
    t=x
    x=y
    y=t
    tx = graph.cypher.execute('match (n) WHERE EXISTS(n.color) and n.name={lb} and toFloat(n.tlx)<={x} and toFloat(n.brx)>={x} and toFloat(n.tly)<={y} and toFloat(n.bry)>={y} RETURN n.block_row,n.block_col,n.color',x=x,y=y,lb=labelname+imgType)
    #print(tx[0],'block')
    color_val = tx[0]['n.color']
    block_row = tx[0]['n.block_row']
    block_col = tx[0]['n.block_col']
    #labelname+imgType
    tx = graph.cypher.execute('match(n:n1) where n.name={name} return n.class_count',name=labelname+'.csv')
    class_count=tx[0]['n.class_count'].split(',')
    tlx=0
    tly=0
    #print('BBLOCK',block_row,block_col)
    for i in range(block_row): tlx = tlx + int(class_count[i])
    for i in range(block_col): tly = tly + int(class_count[i])
    return tlx,tly,block_row,block_col

def getTopLeft_usingBlockId(block_row,block_col,labelname,imgType):
    from py2neo import Graph, Path,authenticate
    authenticate("localhost:7474", "neo4j", "japan123")
    graph = Graph()
    tx = graph.cypher.execute('match(n:n1) where n.name={name} return n.class_count',name=labelname+'.csv')
    class_count=tx[0]['n.class_count'].split(',')
    tlx=0
    tly=0
    #print('BBLOCK',block_row,block_col)
    for i in range(block_row): tlx = tlx + int(class_count[i])
    for i in range(block_col): tly = tly + int(class_count[i])
    return tlx,tly



def blockfilter(x,y,labelname):
    print('-- blockfilter: retrieving pixels associated with the clicked pattern ')
    from py2neo import Graph, Path,authenticate
    authenticate("localhost:7474", "neo4j", "japan123")
    graph = Graph()
    t=x
    x=y
    y=t
    tx = graph.cypher.execute('match (n) WHERE EXISTS(n.color) and n.name={lb} and toFloat(n.tlx)<={x} and toFloat(n.brx)>={x} and toFloat(n.tly)<={y} and toFloat(n.bry)>={y} RETURN n.block_row,n.block_col,n.color',x=x,y=y,lb=labelname)
    print(tx[0],'block')
    color_val = tx[0]['n.color']
    block_row = tx[0]['n.block_row']
    block_col = tx[0]['n.block_col']
    tx = graph.cypher.execute('match (n) WHERE EXISTS(n.color) and n.name={lb} and toFloat(n.block_row)={x} and toFloat(n.block_col)={y} and n.color={c}  RETURN n.brx, n.bry,n.lbl,n.tlx,n.tly,n.color',lb=labelname,x=block_row,y=block_col,c=color_val)
    pixels=[]
    for i in tx:
        tl=[int(i['n.tlx']),int(i['n.tly'])]
        br=[int(i['n.brx']),int(i['n.bry'])]
        color = i['n.color']
        p=Pixel(ast.literal_eval(color),Point(tl[0],tl[1]),Point(br[0],br[1]))
        pixels.extend([p])
    #for i in pixels:
    #    print(str(i))
    print('\t 1. Total pixels in the selected pattern is %d' %(len(pixels)))
    return pixels,color_val

def databasepatternfilter(x,y,labelname):
    print('-- databasepatternfilter: retrieving pixels associated with the clicked pattern ')
    from py2neo import Graph, Path,authenticate
    authenticate("localhost:7474", "neo4j", "japan123")
    graph = Graph()
    t=x
    x=y
    y=t
    tx = graph.cypher.execute('match (n) WHERE EXISTS(n.color) and n.name={lb} and toFloat(n.tlx)<={x} and toFloat(n.brx)>={x} and toFloat(n.tly)<={y} and toFloat(n.bry)>={y} RETURN n.lbl,n.color',x=x,y=y,lb=labelname)
    print(tx[0])
    color_val = tx[0]['n.color']
    tx = tx[0]['n.lbl']
    tx = graph.cypher.execute('match (n) WHERE EXISTS(n.color) and n.name={lb} and toFloat(n.lbl)={x} RETURN n.brx, n.bry,n.lbl,n.tlx,n.tly,n.color',x=int(tx),lb=labelname)

    pixels=[]
    for i in tx:
        tl=[int(i['n.tlx']),int(i['n.tly'])]
        br=[int(i['n.brx']),int(i['n.bry'])]
        color = i['n.color']
        p=Pixel(ast.literal_eval(color),Point(tl[0],tl[1]),Point(br[0],br[1]))
        pixels.extend([p])
    #for i in pixels:
    #    print(str(i))
    print('\t 1. Total pixels in the selected pattern is %d' %(len(pixels)))
    return pixels,color_val


def saveClassLabelColorsInDatabase(datasetName,classLabels):
    print('-- saveClassLabelColorsInDatabase --')
    print(datasetName,classLabels,len(classLabels))
    import seaborn as sns
    x=sns.color_palette("hls", len(classLabels))
    y=[(int(a*255),int(b*255),int(c*255)) for (a,b,c) in x]
    color_list=['%02x%02x%02x' % (r,g,b) for (r,g,b) in y]
    from py2neo import Graph, Path,authenticate,Node,Relationship
    authenticate("localhost:7474", "neo4j", "japan123")
    tx = Graph()
    tx.cypher.execute('MATCH (n:colorClassLabel) where n.name={x} DELETE n',x=datasetName)
    u1=Node('colorClassLabel',name=datasetName)
    tx.create(u1)
    for k in range(len(color_list)):
        u1.properties['H'+color_list[k]] = str(classLabels[k])
        u1.push()

def getClassLabelColorsFromDatabase(datasetName):
    print('--LOADING COLORDICT FROM DATABASE for classLabel')
    from py2neo import  Graph,Path,authenticate,Node,Relationship
    authenticate("localhost:7474","neo4j","japan123")
    tx=Graph()
    opt=tx.cypher.execute('MATCH (n:colorClassLabel) where n.name={x} return keys(n)', x=datasetName)
    allColors=str(opt).split('[')[1].split(']')[0]
    #print(allColors)
    allColors=allColors.replace('\'','')
    allColors=allColors.replace(' ','')
    #print(allColors)
    allColors=allColors.replace('uH','H') #python2
    allColors=allColors.replace('uname','name') #python2
    allColors=allColors.split(',')
    print(allColors)
    allColors.remove('name')
    color_dict={}
    for a in allColors:
        str1='MATCH (n:colorClassLabel) where n.name=\'%s\' return n.%s' %(datasetName,a)
        classLabel=tx.cypher.execute(str1)
        n='n.'+a
        classLabel=classLabel[0][n]
        color_dict[classLabel]='#'+a[1:]
    return color_dict

def filterRowsFromPattern(pixels,rowImgPoints,width,height,scale,grid=False,topLeft_x=0,topLeft_y=0):
    print('-----------------------------------------------------------')
    print(rowImgPoints)
    


def drawPattern(pixels,width,height,scale,grid=False,topLeft_x=0,topLeft_y=0):
    print ('---Draw Pattern---')
    
    #retrieving the image back from quadtree - intialization
    OUTPUT_SCALE=scale
    FILL_COLOR=(255,255,255)
    BORDER_COLOR=(0,100,0)
    #retrieving the image back from quadtree - intialization
    m = OUTPUT_SCALE
    dx, dy = (0,0)#(PADDING, PADDING)
    im = Image.new('RGB', (width * m + dx , height * m + dy))
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, width * m , height * m), BORDER_COLOR,outline=BORDER_COLOR) #(255,255,255)
    draw.rectangle((0, 0, width * m , height * m), FILL_COLOR,outline=FILL_COLOR) #(255,255,255)
    for quad in pixels:
        l, t, r, b = quad.topLeft.x,quad.topLeft.y,quad.bottomRight.x,quad.bottomRight.y
        l=l-topLeft_x
        t=t-topLeft_y
        r=r-topLeft_x
        b=b-topLeft_y
        box = (l * m + dx, t * m + dy, (r+1) * m-1, (b +1)* m-1)
        draw.rectangle(box, quad.color[0],outline=quad.color[0])
    
    del draw
    return im

'''
def drawImage(pixels,width,height,scale,perclustercount=[],class_label=[],color_dict={},grid=False):
    #retrieving the image back from quadtree - intialization
    OUTPUT_SCALE=scale
    FILL_COLOR=(255,255,255)
    #retrieving the image back from quadtree - intialization
    m = OUTPUT_SCALE
    dx, dy = (0,0)#(PADDING, PADDING)
    im = Image.new('RGB', (width * m + dx, height * m + dy))
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, width * m, height * m), FILL_COLOR,outline=(255,255,255))
    for quad in pixels:
        l, t, r, b = quad.topLeft.x,quad.topLeft.y,quad.bottomRight.x,quad.bottomRight.y
        box = (l * m + dx, t * m + dy, (r+1) * m-1, (b +1)* m-1)
        draw.rectangle(box, quad.color[0],outline=(100,0,0))
    del draw
    return im
'''

def drawImage(pixels,width,height,scale,perclustercount=[],class_label=[],color_dict={},grid=False):
    print ('---Draw Image---')
    print(color_dict)
    #retrieving the image back from quadtree - intialization
    OUTPUT_SCALE=scale
    LEGEND_GAP=int((width*scale)/10)
    LEGEND_WIDTH=int((width*scale)/50)
    FILL_COLOR=(255,255,255)
    BORDER_COLOR=(0,100,0)
    #retrieving the image back from quadtree - intialization
    m = OUTPUT_SCALE
    dx, dy = (0,0)#(PADDING, PADDING)
    im = Image.new('RGB', (width * m + dx + LEGEND_GAP, height * m + dy+LEGEND_GAP))
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, width * m + LEGEND_GAP, height * m+LEGEND_GAP), BORDER_COLOR,outline=BORDER_COLOR) #(255,255,255)
    draw.rectangle((0, 0, width * m , height * m), FILL_COLOR,outline=FILL_COLOR) #(255,255,255)
    for quad in pixels:
        l, t, r, b = quad.topLeft.x,quad.topLeft.y,quad.bottomRight.x,quad.bottomRight.y
        box = (l * m + dx, t * m + dy, (r+1) * m-1, (b +1)* m-1)
        draw.rectangle(box, quad.color[0],outline=quad.color[0])
    #DRAWING LEGEND
    #import seaborn as sns
    #x=sns.color_palette("hls", len(perclustercount))
    #y=[(int(a*255),int(b*255),int(c*255)) for (a,b,c) in x]
    #dx,dy = (10,10)
    dx,dy = (0,0)
    prev=0
    for i in range(len(perclustercount)):
        c=perclustercount[i]
        label=class_label[i]
        l,t,r,b=width*m+int(LEGEND_GAP/2), prev , width*m+int(LEGEND_GAP/2)+LEGEND_WIDTH, prev+c*m
        box = (l + dx, t + dy, (r+1) -1, (b +1) -1)
        print(label)
        color_val=color_dict[str(label)]
        draw.rectangle(box, color_val,outline=color_val) #vertical legend
        l,t,r,b=prev,width*m+int(LEGEND_GAP/2) , prev+c*m, width*m+int(LEGEND_GAP/2)+LEGEND_WIDTH
        box = (l + dx, t + dy, (r+1) -1, (b +1) -1)
        draw.rectangle(box, color_val,outline=color_val) #horizontal legend
        prev=prev+c*m

    if grid!=False:
        prev=0
        for c in perclustercount:
            draw.line((0,prev+c*m,sum(perclustercount)*m,prev+c*m),fill=(200,0,0),width=int(LEGEND_WIDTH/4))
            draw.line((prev+c*m,0,prev+c*m,sum(perclustercount)*m),fill=(200,0,0),width=int(LEGEND_WIDTH/4))
            prev=prev+c*m
        draw.line((0,0,0,width*m),fill=(200,0,0),width=int(LEGEND_WIDTH/4))
        draw.line((0,0,width*m,0),fill=(200,0,0),width=int(LEGEND_WIDTH/4))

    del draw
    return im

def saveInfoToDatabase(row,col,name,class_count,class_label):
    print('-- saveInfoToDatabase --')
    print(class_count,class_label)
    from py2neo import Graph, Path,authenticate
    authenticate("localhost:7474", "neo4j", "japan123")
    graph = Graph()
    if(row<300):
        scale=10
    else:
        scale=1
    tx = graph.cypher.execute('MATCH (n:n1) where n.name={x} DELETE n',x=name)
    tx = graph.cypher.execute('create (n:n1 {name:{name}, width:{row},height:{col},scale:{scale},class_count:{class_count},class_label:{class_label},with_legend_width:"",with_legend_height:"" })',name=name,row=row,col=col,scale=scale,class_count=class_count,class_label=class_label)

def updateImageInfo(x,y,name):
    from py2neo import Graph, Path,authenticate
    authenticate("localhost:7474", "neo4j", "japan123")
    graph = Graph()
    tx = graph.cypher.execute('MATCH (n:n1) where n.name={name1} set n.with_legend_width={x},n.with_legend_height={y}',name1=name,x=x,y=y)
    return

def getImageParams(datasetname):
    from py2neo import Graph, Path,authenticate
    authenticate("localhost:7474", "neo4j", "japan123")
    graph = Graph()
    tx = graph.cypher.execute('match (n:n1) where n.name={d} return n.width, n.height, n.scale, n.class_count, n.class_label',d=datasetname);
    width=int(tx[0]['n.width'])
    height=int(tx[0]['n.height'])
    scale=int(tx[0]['n.scale'])
    class_count=tx[0]['n.class_count']
    class_label=tx[0]['n.class_label']
    return width,height,scale,class_count,class_label

def getImageParams_pattern(datasetname):
    from py2neo import Graph, Path,authenticate
    authenticate("localhost:7474", "neo4j", "japan123")
    graph = Graph()
    tx = graph.cypher.execute('match (n:n1) where n.name={d} return n.with_legend_width, n.with_legend_height, n.scale, n.class_count, n.class_label',d=datasetname);
    width=int(tx[0]['n.with_legend_width'])
    height=int(tx[0]['n.with_legend_height'])
    scale=int(tx[0]['n.scale'])
    class_count=tx[0]['n.class_count']
    class_label=tx[0]['n.class_label']

    return width,height,scale,class_count,class_label


def getBlockDimension(datasetname,row_bid,col_bid):
    print('----- getBlockDimension -----')
    print('params: ',datasetname,row_bid,col_bid)
    from py2neo import Graph, Path,authenticate
    authenticate("localhost:7474", "neo4j", "japan123")
    graph = Graph()
    tx = graph.cypher.execute('match (n:n1) where n.name={d} return n.class_count',d=datasetname);
    class_count=tx[0]['n.class_count']
    class_count=class_count.split(',')
    print(class_count)
    row_width=int(class_count[row_bid])
    col_width=int(class_count[col_bid])
    return row_width,col_width

if __name__=='__main__':
    #src='/home/ayushi/Ayushi/thesis/2-image-indexing/code/quadTree-region-labelling-neo4j/img_bea.png'
    src='/home/ayushi/Ayushi/github/visualization_projects/1-add-dim/static/output/img_bea.png'
    x=Image.open(src)
    #saveMatrixToDatabase(x,'','','','')
    q=quadTree(x,Point(0,0),Point(x.size[0]-1,x.size[1]-1))
    splitBlock(q,x)
    pixels=get_leaf_nodes(q)
    im=drawImage(pixels,x.size[0],x.size[1],10)
    im.save('quad_visual.png')
