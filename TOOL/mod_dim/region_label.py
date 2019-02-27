import pandas as pd
from PIL import Image,ImageDraw
import numpy as np
import seaborn as sns

def getIfromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    if(red==255 and green==255 and blue==255): return 0
    RGBint = (red<<16) + (green<<8) + blue
    return RGBint

#NOT REQUIRED, REDUNDANT FUNCTION
def visualize_regions_v2(pixels,width,height,scale):
    OUTPUT_SCALE=scale
    FILL_COLOR=(255,255,255)
    #retrieving the image back from quadtree - intialization
    OUTPUT_SCALE=10
    FILL_COLOR=(255,255,255)
    m = OUTPUT_SCALE
    dx, dy = (0,0)#(PADDING, PADDING)
    im = Image.new('RGB', (width * m + dx, height * m + dy))
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, width * m+100, height * m+100), FILL_COLOR,outline=FILL_COLOR)
    c=1
    for quad in pixels:
        l, t, r, b = quad.tlx,quad.tly,quad.brx,quad.bry
        box = (l * m + dx, t * m + dy, (r+1) * m-1, (b +1)* m-1)
        draw.rectangle(box, quad.color,outline=quad.color)
        #im.save('img'+str(c)+'.png')
        c+=1
    del draw
    return im


def visualize_regions(lbl):
    colorList=sns.color_palette("hls", len(np.unique(lbl)))
    colorList=[(int(a*255),int(b*255),int(c*255)) for (a,b,c) in colorList]
    OUTPUT_SCALE=10
    width=lbl.shape[0]
    height=lbl.shape[1]
    FILL_COLOR=(255,255,255)
    #retrieving the image back from quadtree - intialization
    OUTPUT_SCALE=10
    width=lbl.shape[0]
    height=lbl.shape[1]
    FILL_COLOR=(255,255,255)
    m = OUTPUT_SCALE
    dx, dy = (0,0)#(PADDING, PADDING)
    im = Image.new('RGB', (width * m + dx, height * m + dy))
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, width * m+100, height * m+100), FILL_COLOR,outline=FILL_COLOR)
    for i in range(width):
        for j in range(height):
            l, t, r, b = i,j,i,j#j,i,j+1,i+1
            box = (l * m + dx, t * m + dy, (r+1) * m-1, (b +1)* m-1)
            if(lbl[i][j]!=0):
                draw.rectangle(box, colorList[int(lbl[i][j])],outline=colorList[int(lbl[i][j])])
                #im.save('img'+str(lbl[i][j])+'.png')
    del draw
    return im

def regionLabelling(hm):
    y=1
    lbl=np.zeros((hm.shape[0],hm.shape[1]))
    c=1
    equ={}
    for i in range(0,hm.shape[0]):
        for j in range(0,hm.shape[1]):
            if hm[i][j]==0: continue
            if(i!=0 and j!=0 and hm[i-1][j]==hm[i][j-1] and hm[i-1][j]==hm[i][j]):
                if lbl[i-1][j]!=lbl[i][j-1]: equ[lbl[i-1][j]]=lbl[i][j-1]
                lbl[i][j]=lbl[i-1][j]
            elif(i!=0 and hm[i-1][j]==hm[i][j]): lbl[i][j]=lbl[i-1][j]
            elif(j!=0 and hm[i][j-1]==hm[i][j]): lbl[i][j]=lbl[i][j-1]
            else:
                lbl[i][j]=c
                c=c+1
    for k in equ:
        #print(k,equ[k])
        lbl[lbl == k] = equ[k]

    c=1
    for k in np.unique(lbl):
        if k!=0:
            lbl[lbl==k]=c
            c=c+1

    return lbl

def regionLabelling_8(hm):
    y=1
    lbl=np.zeros((hm.shape[0],hm.shape[1]))
    c=1
    equ={}
    for i in range(0,hm.shape[0]):
        for j in range(0,hm.shape[1]):
            #print(hm[i][j],hm[i][j]==0)
            if hm[i][j]==0: continue
            if(i!=0 and j!=0 and (j+1)!=hm.shape[1] and hm[i-1][j+1]==hm[i][j] and hm[i][j-1]==hm[i][j]):
                if lbl[i][j-1]!=lbl[i-1][j+1]: equ[lbl[i][j-1]]=lbl[i-1][j+1]
                lbl[i][j]=lbl[i][j-1]
            elif(i!=0 and j!=0 and hm[i-1][j]==hm[i][j-1] and hm[i-1][j]==hm[i][j]):
                if lbl[i-1][j]!=lbl[i][j-1]: equ[lbl[i-1][j]]=lbl[i][j-1]
                lbl[i][j]=lbl[i-1][j]
            elif(i!=0 and j!=0 and (j+1)!=hm.shape[1] and hm[i-1][j-1]==hm[i][j] and hm[i-1][j+1]==hm[i][j]):
                if lbl[i-1][j-1]!=lbl[i-1][j+1]: equ[lbl[i-1][j-1]]=lbl[i-1][j+1]
                lbl[i][j]=lbl[i-1][j+1]
            elif(i!=0 and hm[i-1][j]==hm[i][j]):
                lbl[i][j]=lbl[i-1][j]
            elif(j!=0 and hm[i][j-1]==hm[i][j]):
                lbl[i][j]=lbl[i][j-1]
            elif(i!=0 and j!=0 and hm[i-1][j-1]==hm[i][j]):
                lbl[i][j]=lbl[i-1][j-1]
            elif(i!=0 and (j+1)!=hm.shape[1] and hm[i-1][j+1]==hm[i][j]):
                lbl[i][j]=lbl[i-1][j+1]
            else:
                lbl[i][j]=c
                c=c+1
    #for j in range(0,hm.shape[0]):
    #    print(lbl[0][j])
    #print(equ)
    for k in equ:
        lbl[lbl == k] = equ[k]

    c=1
    for k in np.unique(lbl):
        if k!=0:
            lbl[lbl==k]=c
            c=c+1
    return lbl

if __name__=='__main__':
    src='/home/ayushi/Ayushi/github/visualization_projects/1-add-dim/static/output/img_bea.png'
    x=np.asarray(Image.open(src))
    y=np.zeros((x.shape[0],x.shape[1]))
    for i in range(x.shape[0]):
        for j in range(x.shape[0]):
            y[i][j]=getIfromRGB(x[i][j])

    lbl=regionLabelling_8(y)
    lbl=pd.DataFrame(lbl)
    lbl.to_csv('lbl.csv',index=False);
    im=visualize_regions(lbl)
    im.save('img.png')
    #print(lbl[0:10,0:30],len(np.unique(lbl)))
