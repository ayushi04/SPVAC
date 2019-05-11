from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.Integer, nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, name="", phone="", password="", email=""):
        self.email = email
        self.phone = phone
        self.name = name
        self.password = password

    def __repr__(self):
        return "<User %s %s>" % (self.id, self.name)


"""
This table stores the color associated with a given subspace.
The advantage of maintaining this table is that the same color map
is maintained across all Heidi Images
"""
class SubspaceColorMap(db.Model, UserMixin):
    __tablename__ = 'subspace_color_map'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    dataset = db.Column(db.String(100), nullable = False)
    color = db.Column(db.String(10), nullable = False)
    subspace = db.Column(db.String(100), nullable = False) 
    print("1. TODO : change subspace type to blob")

    def __init__(self, dataset='', color='', subspace=''):
        self.dataset = dataset
        self.color = color
        self.subspace = subspace

    def __repr__(self):
        return "<SubspaceColorMap %s %s %s>" %(self.dataset, self.color, self.subspace)

class Dataset(db.Model, UserMixin):
    __tablename__='dataset'
    name = db.Column(db.String(50), primary_key = True)
    storagePath = db.Column(db.String(100), nullable = False, unique = True)
    content = db.Column(db.BLOB(), nullable = False, unique = True) # cleaned file

    def __init__(self, name, storagePath, content):
        self.name = name
        self.storagePath = storagePath
        self.content = content

    def __repr__(self):
        return "<Dataset %s %s>" %(self.name, self.content)

"""
class ColorMap(db.Model, UserMixin):
    __tablename__='colormap'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    color = db.Column(db.String(10), nullable = False)
    subspace = db.Column(db.String(50), nullable = False)
    dataset = db.Column(db.String(50), nullable = False) #ForeignKey("dataset.name"), 

    def __init__(self, color, subspace, dataset):
        self.color = color
        self.subspace = subspace
        self.dataset = dataset

    def __repr__(self):
        return "< ColorMap %s %s >" %(self.color, self.subspace)
"""

class SubspaceHeidiMap(db.Model, UserMixin):
    __tablename__='subspace_heidi_map'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    subspace = db.Column(db.String(50), nullable = False)
    dataset = db.Column(db.String(50), nullable = False) #ForeignKey("dataset.name"), 
    heidiMatrix = db.Column(db.BLOB(), nullable = False)
    heidiImage = db.Column(db.BLOB(), nullable = False)
    
    def __init__(self, subspace, dataset, heidiMatrix, heidiImage):
        self.subspace = subspace
        self.dataset = dataset
        self.heidiMatrix = heidiMatrix
        self.heidiImage = heidiImage

    def __repr__(self):
        return "< SubspaceHeidiMap %s %s %s >" %(self.subspace, self.dataset, self.heidiMatrix)




"""
This table stores the image and the continious regions in the image
Each region is assigned a unique label
"""
#t1 in neo4j
class Image(db.Model, UserMixin):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    tlx = db.Column(db.Integer,nullable=False)
    tly = db.Column(db.Integer,nullable=False)
    brx = db.Column(db.Integer,nullable=False)
    bry = db.Column(db.Integer,nullable=False)
    color = db.Column(db.String(400),nullable=False)
    label = db.Column(db.Integer,nullable=False)
    block_col = db.Column(db.Integer,nullable=False)
    block_row = db.Column(db.Integer,nullable=False)
    #email = db.Column(db.String(100), unique=True, nullable=False)
    #name = db.Column(db.String(100), nullable=False)
    #phone = db.Column(db.Integer, nullable=False, unique=True)
    #password = db.Column(db.String(80), nullable=False)

    def __init__(self, name="", tlx="", tly="", brx="",bry="",color="",block_row="",block_col=""):
        self.tlx = tlx
        self.tly = tly
        self.name = name
        self.brx = brx
        self.bry = bry

    def __repr__(self):
        return "<image %s %s>" % (self.id, self.name)


'''
class Image(db.Model, UserMixin):
    __table__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    tlx = db.Column(db.Integer,nullable=False)
    tly = db.Column(db.Integer,nullable=False)
    brx = db.Column(db.Integer,nullable=False)
    bry = db.Column(db.Integer,nullable=False)
    color = db.Column(db.String(400),nullable=False)
    block_col = db.Column(db.Integer,nullable=False)
    block_row = db.Column(db.Integer,nullable=False)

    def __init__(self, name="", tlx="", tly="", brx="",bry="",color="",block_row="",block_col=""):
        self.tlx = tlx
        self.tly = tly
        self.name = name
        self.brx = brx
'''    