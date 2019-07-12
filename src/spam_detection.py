""" Spam detection """
import pandas as pd
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, \
recall_score, f1_score


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


# Load spam samples
df = read_csv(
    file_address='../data/csv/spam.csv',
    names=['category', 'text'],
    usecols=[0, 1],
    skiprows=1,
    )


# Prepare categories for processing
df['category'] = df['category'].map({'ham': 0, 'spam': 1})

print(df.shape)
print(df.head())


# Split data into training and testing set
split = train_test_split(
    df['text'],
    df['category'],
    test_size=0.3
    )

training_words, testing_words, training_cat, testing_cat = split


# Extract features (create Bag of Words)
count_vector = CountVectorizer(
    lowercase=True, 
    stop_words=stopwords.words('english')
    )
training_set = count_vector.fit_transform(training_words)
testing_set = count_vector.transform(testing_words)

print('Training set {}'.format(training_set.shape))
print('Testing set {}'.format(testing_set.shape))


# Create model using multinomial naive bayes
naive_bayes_model = MultinomialNB(alpha=0.5)
naive_bayes_model.fit(training_set, training_cat)


# Make predictions for testing data
predictions = naive_bayes_model.predict(testing_set)


# Verify model quality
print('Accuracy: {}'.format(accuracy_score(testing_cat, predictions)))
print('Precision: {}'.format(precision_score(testing_cat, predictions)))
print('Recall: {}'.format(recall_score(testing_cat, predictions)))
print('f1: {}'.format(f1_score(testing_cat, predictions)))
