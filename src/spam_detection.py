""" Spam detection """
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from collections import defaultdict


def read_csv(file_address, names=None, usecols=None, skiprows=0, nrows=None):
    with open(file_address,'r') as f:
        df = pd.read_csv(
            filepath_or_buffer=f,
            names=names,
            usecols=usecols,
            skiprows=skiprows,
            nrows=nrows
        )

    return df


def normalize_text(text):
    t = text.casefold()
    t = re.sub(r'[^a-zA-Z0-9]',' ',t)

    return t


def remove_stop_words(words):
    stop_words = stopwords.words('english')
    cleaned_words = [w for w in words if w not in stop_words]

    return cleaned_words


if __name__ == '__main__':

    # Load spam samples
    df = read_csv(
        file_address='../data/csv/spam.csv',
        names=['category', 'text'],
        usecols=[0, 1],
        skiprows=1,
        nrows=5
    )

    # Prepare data for processing
    df['category'] = df['category'].map({'ham': 0, 'spam': 1})
    df['text'] = df['text'].apply(normalize_text)
    df['text'] = df['text'].apply(nltk.word_tokenize)
    df['text'] = df['text'].apply(remove_stop_words)

    print(df.shape)
    print(df.head())
