""" Spam detection """
import pandas as pd

def read_csv(file_address,names=None,usecols=None,nrows=None):
    with open(file_address,'r') as f:
        df = pd.read_csv(f,names=names,usecols=usecols,nrows=nrows)

    return df

if __name__ == '__main__':

    # Load useful info sample
    df = read_csv(
                file_address='../data/csv/spam.csv',
                names=['category','text'],
                usecols=[0,1],
                nrows=5
                )
    
    # Prepare for processing
    df['category'] = df['category'].map({'ham':0,'spam':1})

    print(df.shape)
    print(df.head())
