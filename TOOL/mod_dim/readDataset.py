import pandas as pd
#from app.mod_home import createDirHelper as cdh
import logging
import numpy as np

class ReadDatasetCls:
    datapath=""
    inputData=""
    row=""
    col=""
    feature_vector_dict=""
    classLabel_numeric=""
    class_label_dict=""
    feature_vector=""

    def getRow(self):
        print('----READDATASET : getRow----')
        return str(self.row)

    def getCol(self):
        print('----READDATASET : getCol----')
        return str(self.col)

    def getInputData(self):
        print('----READDATASET : getInputData----')
        t=self.feature_vector
        t['classLabel']=self.classLabel_numeric
        return t

    def getClassLabelDict(self):
        print('----READDATASET : getClassLabelDict----')
        return self.class_label_dict

    #METHOD TO SEPERATE CLASSLABEL FROM FEATURE_VECTOR IF IT EXISTS, OTHERWISE CREATE A CLASSLABEL DATAFRAME WITH '1' IN ALL ROWS
    def sep_fv_label(self,classlabel):
        print('----READDATASET : sep_fv_label----')
        if(classlabel.lower()=="yes"):
            self.feature_vector=self.inputData.iloc[:,0:self.col-1]
            self.classLabel_given=self.inputData.iloc[:,self.col-1]
            self.classLabel_numeric=self.classLabel_given.astype('category').cat.codes
            self.col=self.col-1
            self.class_label_dict = dict(zip(self.classLabel_numeric, self.classLabel_given))
        else:
            self.feature_vector=self.inputData.iloc[:,0:self.col]
            self.classLabel_given=np.ones_like(self.inputData.iloc[:,0])
            self.classLabel_numeric=np.ones_like(self.inputData.iloc[:,0])
            self.class_label_dict=dict(zip(self.classLabel_numeric, self.classLabel_given))

    #METHOD TO READ CLEANED DATA AS INPUT
    #ASSUMPTION: INPUT DATASET IS NUMERIC EXCEPT CLASSLABEL AND THERE IS NO MISSING VALUE
    def readDataset(self,filepath,classlabel="yes") :
        print('----READDATASET : readDataset----')
        #print('classlabel',classlabel)
        logging.info('Reading dataset from path %s..',filepath)
        self.datapath=filepath
        try:
            self.inputData=pd.read_csv(filepath_or_buffer=filepath,sep=',',index_col=None)
            self.row=self.inputData.shape[0]
            self.col=self.inputData.shape[1]
            self.feature_vector_dict={}
            self.sep_fv_label(classlabel)
            logging.info('Read %s dataset sucessfully..' %(cdh.getFileNameFromDirPath(filepath)))
            logging.info('It has %d rows and %d columns' %(self.row,self.col))
            return self.feature_vector,self.classLabel_numeric,self.class_label_dict,self.feature_vector_dict, self.row, self.col
        except FileNotFoundError:
            logging.exception('Input file path in method readDataset is invalid!!!')
            raise Exception('Input file path in method readDataset is invalid!!!')
        except :
            logging.exception('Error occured in readDataset method!!!')
            print('Error occured in readDataset method of read_dataset class (file : read_dataset.py)!!!')
            #raise Exception('Error occured in readDataset method of read_dataset class (file : read_dataset.py)!!!')
        return -1

    def printDatasetInfo(self):
        print('----READDATASET : printDatasetInfo----')
        try :
            if(self.row!=""):
                print('------------------------------------------------------')
                print('Given dataset has %d number of records' %(self.row))
                print('Number of attributes are %d' %(self.col))
                print('Columns are: %s' %(str(self.feature_vector.columns)))
                print('classLabel_numeric is :',set(self.classLabel_numeric))
                print('class_label_dict is ')
                print(self.class_label_dict)
                print('feature_vector_dict is ')
                print(self.feature_vector_dict)
                print('number of rows : %d and cols : %d' %(self.row,self.col))
                print('------------------------------------------------------')
            else:
                print('Dataset not read!!! Please read dataset first!!!')
        except :
            logging.exception('Error occured in printDatasetInfo method of read_dataset class (file : read_dataset.py)!!!')
            print('Error occured in printDatasetInfo method of read_dataset class (file : read_dataset.py)!!!')
            #raise Exception('Error occured in readDataset method of read_dataset class (file : read_dataset.py)!!!')

if __name__=='__main__':
    robj=ReadDatasetCls()
    robj.readDataset('../static/dataset/iris.csv')
    fv=robj.getInputData()
    fv.to_csv('../static/dataset/iris_processed.csv',index=False)
