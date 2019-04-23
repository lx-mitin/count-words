""" Spam detection """
import pandas as pd

def read_csv(file_address):
    with open(file_address,'r') as f:
        df = pd.read_csv(f)

    return df

if __name__ == '__main__':
    df = read_csv('./data/csv/spam.csv')
    print(df.head(10))