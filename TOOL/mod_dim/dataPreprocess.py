import pandas as pd

if __name__=='__main__':
    df=pd.read_csv('../static/dataset/student-mat.csv',sep=',')
    mylist=['school', 'sex', 'address', 'famsize', 'Pstatus',
       'Mjob', 'Fjob', 'reason', 'guardian', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery',
       'higher', 'internet', 'romantic', 'Dalc',
       'Walc', 'health', 'absences', 'G1', 'G2', 'G3']
    for c in mylist:
        df[c] = df[c].astype('category')
    print(df.columns)
    cat_columns = df.select_dtypes(['category']).columns
    df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)
    df.to_csv('../static/dataset/student-mat-pro.csv',index=False)
