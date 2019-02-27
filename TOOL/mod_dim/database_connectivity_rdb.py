from PIL import Image,ImageDraw,ImageFilter
from numpy import *
from mod_dim import region_label as rg
from models import ImageDB,Legend,TopLegend,ImageInfo
import pandas as pd
import ast
from app import db

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

# SAVING ENTIRE QUAD TREE TO DATABASE
# SAVE ONLY THE LEAF NODES OF QUAD TREE IN DATABASE
def saveMatrixToDatabase_leaf(image,bit_subspace,outputPath,sorted_data,lbl,labelname='n1'):
    #write code here to save to database
    print('---CREATING QUADTREE FOR IMAGE----')
    print(sorted_data.columns)
    q=quadTree(image,Point(0,0),Point(image.size[0]-1,image.size[1]-1))
    splitBlock(q,image)
    def preorder1(start):
        if(start==None): return
        if(len(start.pixel.color)==1):
            color=str(start.pixel.color[0])
            block_row = int(sorted_data.iloc[int(start.pixel.topLeft.x),-1])
            block_col = int(sorted_data.iloc[int(start.pixel.topLeft.y),-1])
            u1=ImageDB(name=labelname,tlx=str(start.pixel.topLeft.x),tly=str(start.pixel.topLeft.y),brx=str(start.pixel.bottomRight.x),bry=str(start.pixel.bottomRight.y),color=color,lbl=lbl[start.pixel.topLeft.y][start.pixel.topLeft.x],block_row=block_row,block_col=block_col)
            db.session.add(u1)
            temp=lbl[start.pixel.topLeft.y:start.pixel.bottomRight.y+1,start.pixel.topLeft.x:start.pixel.bottomRight.x+1]
            x=unique(temp)
            #if(len(x)>1):
            #    print("ERROR:",start.pixel,x)
            #tx.create(u1)
            #tx.merge(u1)
        preorder1(start.left)
        preorder1(start.mid1)
        preorder1(start.mid2)
        preorder1(start.right)
    #n = db.labels.create("tmp2")
    print('----SAVING QUADTREE IN DATABASE---')
    preorder1(q)
    print('---done---')
    db.session.commit()
    #tx.commit()




def deleteAllNodes(labelname='image'):
    x = ImageDB.query.filter_by(name=labelname)
    print(x)
    for i in x:
        db.session.delete(i)
    db.session.commit()


def drawImage(pixels,width,height,scale,perclustercount=[],class_label=[],color_dict={},grid=False,blurr=False):
    print ('---Draw Image---')
    print(color_dict)

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
    if blurr==True:
        draw.rectangle((0, 0, width * m + LEGEND_GAP, height * m+LEGEND_GAP), FILL_COLOR,outline=FILL_COLOR) #(255,255,255)
    else:
        draw.rectangle((0, 0, width * m + LEGEND_GAP, height * m+LEGEND_GAP), BORDER_COLOR,outline=BORDER_COLOR) #(255,255,255)
    draw.rectangle((0, 0, width * m , height * m), FILL_COLOR,outline=FILL_COLOR) #(255,255,255)
    for quad in pixels:
        l, t, r, b = quad.tlx,quad.tly,quad.brx,quad.bry
        box = (l * m + dx, t * m + dy, (r+1) * m-1, (b +1)* m-1)
        #print(quad.color)
        draw.rectangle(box, quad.color,outline=quad.color)

    if blurr==True:
        im= im.filter(ImageFilter.GaussianBlur(radius=10))
        del draw
        return im

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
    #im1 = im.filter(ImageFilter.BLUR)
    return im

def getbackground(labelname,datasetName,grid=False):
    pixels = ImageDB.query.filter_by(name=labelname)
    width,height,scale,class_count,class_label=getImageParams(datasetName)
    class_count=class_count.split(',')
    perclustercount=[int(i) for i in class_count]
    class_label=class_label.split(',')
    class_label=[int(i) for i in class_label]
    #print('pppp1',width,height,scale)
    color_dict=getColorFromTopLegend(datasetName)
    im = drawImage(pixels,width,height,scale,perclustercount,class_label,color_dict,grid,blurr=True)
    return im

    


# SAVE COLOR DICTIONARY TO DATABASE (saving legend)
def saveColorToDatabase(colorDict,datasetname):
    #write code here to save to database
    print('---SAVING COLOR DICT IN DATABASE----')
    
    x = Legend.query.filter_by(name=datasetname)
    print(x)
    for i in x:
        db.session.delete(i)
    db.session.commit()

    print(colorDict)
    for c in colorDict:
        u1=Legend(name=datasetname,color=c,subspace=colorDict[c])
        db.session.add(u1)
    db.session.commit()

def loadColorFromDatabase(datasetName):
    print('---LOADING COLORDICT FROM DATABASE----')
    
    x = Legend.query.filter_by(name=datasetName)
    allSubspace=set([])
    color_dict={}
    for i in x:
        subspace=ast.literal_eval('['+i.subspace+']')
        color_dict[i.color]=subspace
        for j in subspace:
            #print(i)
            allSubspace.add(tuple(j))
    print('--end--')
    return color_dict,list(allSubspace)


def saveClassLabelColorsInDatabase(datasetName,classLabels):
    x = TopLegend.query.filter_by(name=datasetName)
    print(x)
    for i in x:
        db.session.delete(i)
    db.session.commit()
    
    print('-- saveClassLabelColorsInDatabase --')
    print(datasetName,classLabels,len(classLabels))
    import seaborn as sns
    x=sns.color_palette("hls", len(classLabels))
    y=[(int(a*255),int(b*255),int(c*255)) for (a,b,c) in x]
    color_list=['#%02x%02x%02x' % (r,g,b) for (r,g,b) in y]
    for k in range(len(color_list)):
        u1=TopLegend(name=datasetName,color=color_list[k],classLabel=str(classLabels[k]))
        db.session.add(u1)
    db.session.commit()

def getColorFromTopLegend(datasetName):
    print('--LOADING COLORDICT FROM DATABASE for classLabel')
    x=TopLegend.query.filter_by(name=datasetName)
    color_dict={}
    for i in x:
        color_dict[i.classLabel]=i.color
    return color_dict
    '''
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
    '''
    return {}

# FETCH ONLY THOSE NODES WITH THE GIVEN COLOR IN DATABASE
def databasefilter(labelname,color='ALL'):
    print('--Database filter ALL/color--')
    print(color)
    if(color!='ALL'):
        #color='[\''+color+'\']'
        pixels = ImageDB.query.filter_by(name=labelname,color=color)
    else:
        pixels = ImageDB.query.filter_by(name=labelname)
    print(pixels)
    #print('/t 1. retrieved all pixels. Total count is %d' %(len(pixels)))
    return pixels

def saveInfoToDatabase(row,col,name,class_count,class_label):
    print('-- saveInfoToDatabase --')
    print(class_count,class_label)
    if(row<300):
        scale=10
    else:
        scale=1

    x = ImageInfo.query.filter_by(name=name)
    for i in x:
        db.session.delete(i)
    db.session.commit()

    tx = ImageInfo(name,row,col,scale,class_count,class_label)
    db.session.add(tx)
    db.session.commit()

def getImageParams(datasetName):
    tx = ImageInfo.query.filter_by(name=datasetName)
    print('txt',tx)
    width=int(tx[0].width)
    height=int(tx[0].height)
    scale=int(tx[0].scale)
    class_count=tx[0].class_count
    class_label=tx[0].class_label
    return width,height,scale,class_count,class_label
    
def updateImageInfo(x,y,name):
    t=ImageInfo.query.filter_by(name=name)[0]
    t.with_legend_width=x
    t.with_legend_height=y
    db.session.commit()
    return

def getTopLeftCoordinates_Grid(x,y,labelname,datasetName='image'):
    print('-- getTopLeftCoordinates_Grid: retrieving top left coordinates of grid ')
    tx = ImageDB.query.filter(ImageDB.name==labelname,ImageDB.tlx<=x,ImageDB.brx>=x,ImageDB.tly<=y,ImageDB.bry>=y);
    print(tx[0],size(tx))
    color_val = tx[0].color
    block_row = tx[0].block_row
    block_col = tx[0].block_col
    #labelname+imgType
    tx = ImageInfo.query.filter_by(name=datasetName)
    class_count=tx[0].class_count.split(',')
    print(class_count)
    tlx=0
    tly=0
    print('BBLOCK',block_row,block_col)
    for i in range(block_row): 
        print(class_count[i])
        tlx = tlx + int(class_count[i])
    for i in range(block_col): tly = tly + int(class_count[i])
    return tlx,tly,block_row,block_col

def databasepatternfilter(x,y,labelname):
    tx = ImageDB.query.filter(ImageDB.name==labelname,ImageDB.tlx<=x,ImageDB.brx>=x,ImageDB.tly<=y,ImageDB.bry>=y);
    print(tx[0],size(tx))
    color_val = tx[0].color
    lbl = tx[0].lbl
    pixels = ImageDB.query.filter_by(name=labelname, lbl=lbl)
    return pixels,color_val

def blockfilter(x,y,labelname):
    print('-- blockfilter: retrieving pixels associated with the clicked pattern ')
    tx = ImageDB.query.filter(ImageDB.name==labelname,ImageDB.tlx<=x,ImageDB.brx>=x,ImageDB.tly<=y,ImageDB.bry>=y);
    print(tx[0],size(tx))
    color_val = tx[0].color
    block_row = tx[0].block_row
    block_col = tx[0].block_col
    pixels = ImageDB.query.filter_by(name=labelname,block_col=block_col,block_row=block_row,color=color_val)
    return pixels,color_val


def getCoordinates(pixels,sortedPath,unique=True):
    rowPointsIndex=[]
    colPointsIndex=[]
    pair=[]
    x=pd.read_csv(sortedPath,index_col=0)
    for p in pixels:
        tlx=p.tlx
        tly=p.tly
        brx=p.brx
        bry=p.bry
        for i in range(tlx,brx+1):
            for j in range(tly,bry+1):
                rowPointsIndex.extend([i])
                colPointsIndex.extend([j])
                pair.extend([str(i)+':'+str(j)])
                #pair.extend([x.index.get_values()[i]+':'+x.index.get_values()[j]])
        #print(rowPointsIndex,colPointsIndex,tl,br)
    if(unique==True):
        rowPointsIndex=list(set(rowPointsIndex))
        colPointsIndex=list(set(colPointsIndex))
    print('---',len(rowPointsIndex),len(colPointsIndex))
    rowPoints = x.iloc[rowPointsIndex,:]
    colPoints = x.iloc[colPointsIndex,:]
    return rowPoints,colPoints
