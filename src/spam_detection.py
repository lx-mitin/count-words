""" Spam detection """
import pandas as pd

def read_csv(file_address,nrows=None):
    with open(file_address,'r') as f:
        df = pd.read_csv(f,nrows=nrows)

    return df

if __name__ == '__main__':
    df = read_csv('../data/csv/spam.csv',5)

    df = df.drop(df.columns[[2,3,4]],1)
    df = df.rename(columns={'v1':'category','v2':'text'})

    df['category'] = df['category'].map({'ham':0,'spam':1})

    print(df.shape)
    print(df.head())
