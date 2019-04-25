""" Spam detection """
import pandas as pd

def read_csv(file_address):
    with open(file_address,'r') as f:
        df = pd.read_csv(f)

    return df

if __name__ == '__main__':
    df = read_csv('./data/csv/spam.csv')
    df = df.drop(df.columns[[2,3,4]],1)
    df = df.rename(columns={'v1':'category','v2':'text'})

    print(df.head(10))
