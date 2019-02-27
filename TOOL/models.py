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


class ImageDB(db.Model, UserMixin):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    tlx = db.Column(db.Integer,nullable=False)
    tly = db.Column(db.Integer,nullable=False)
    brx = db.Column(db.Integer,nullable=False)
    bry = db.Column(db.Integer,nullable=False)
    color = db.Column(db.String(400),nullable=False)
    lbl = db.Column(db.Integer,nullable=False)
    block_col = db.Column(db.Integer,nullable=False)
    block_row = db.Column(db.Integer,nullable=False)
    def __init__(self, name="", tlx="", tly="", brx="",bry="",color="",lbl='',block_row="",block_col=""):
        self.tlx = tlx
        self.tly = tly
        self.name = name
        self.color=color
        self.brx = brx
        self.bry=bry
        self.lbl=lbl
        self.block_row=block_row
        self.block_col=block_col

class Legend(db.Model, UserMixin):
    __tablename__ = 'legend'
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    color = db.Column(db.String(20),nullable=False)
    subspace = db.Column(db.String(200),nullable=False)

    def __init__(self,name,color,subspace):
        self.name=name
        self.color=color
        self.subspace=subspace

class TopLegend(db.Model,UserMixin):
    __tablename__='toplegend'
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    color = db.Column(db.String(10),nullable=False)
    classLabel = db.Column(db.String(20),nullable=False)

    def __init__(self,name,color,classLabel):
        self.name=name
        self.color=color
        self.classLabel=classLabel

class ImageInfo(db.Model,UserMixin):
    __tablename__='imageinfo'
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    width = db.Column(db.Integer,nullable=False)
    height = db.Column(db.Integer,nullable=False)
    scale = db.Column(db.Integer,nullable=False)
    class_count = db.Column(db.String(100),nullable=False)
    class_label = db.Column(db.String(100),nullable=False)
    with_legend_width = db.Column(db.Integer,nullable=False)
    with_legend_height = db.Column(db.Integer,nullable=False)

    def __init__(self,name,row,col,scale,class_count,class_label,with_legend_width='',with_legend_height=''):
        self.name=name
        self.width=row
        self.height=col
        self.scale=scale
        self.class_count=class_count
        self.class_label=class_label
        self.with_legend_width=with_legend_width
        self.with_legend_height=with_legend_height
