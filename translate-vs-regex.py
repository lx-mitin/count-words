"""Compare translate vs regex for text normalization task"""
from string import punctuation
from re import sub
from datetime import datetime
import numpy as np

# replace punctuation characters with space by using regular expression
def normalize_regex(text):
    
    return sub(r'[^а-яА-Я0-9]',' ',text)

# replace punctuation characters with space by using regular expression (letter are preliminary lowered)
def lower_regex(text):
    
    return sub(r'[^а-я0-9]',' ',text)
# replace punctuation characters with space by using translate
def normalize_trans(text):

    translation_dictionary = {p:' ' for p in punctuation}
    return text.translate(text.maketrans(translation_dictionary))

# remove punctuation characters by using translate
def remove_punctuation_translate(text):
    return text.translate(text.maketrans('','',punctuation))


#  compare translate vs regex
def translate_vs_regex_compare():

    with open('roadside-picnic-ru.txt','r') as f:

        text = f.read()
        text = text.casefold()

    regex_times = []
    lower_times = []
    trans_times = []
    remove_times = []

    for i in range(10):

        time = datetime.now()
        t1 = normalize_regex(text)
        delta_time = datetime.now() - time
        regex_times.append(delta_time.total_seconds())

        t2 = text.casefold()
        time = datetime.now()
        t2 = lower_regex(text)
        delta_time = datetime.now() - time
        lower_times.append(delta_time.total_seconds())

        time = datetime.now()
        t3 = normalize_trans(text)
        delta_time = datetime.now() - time
        trans_times.append(delta_time.total_seconds())

        time = datetime.now()
        t4 = remove_punctuation_translate(text)
        delta_time = datetime.now() - time
        remove_times.append(delta_time.total_seconds())

    print('regex, avg: {}\t std dev: {}'
          .format(np.average(regex_times),np.std(regex_times)))
    print('regex-lower,  avg: {}\t std dev: {}'
          .format(np.average(lower_times),np.std(lower_times)))
    print('translate-replace,  avg: {}\t std dev: {}'
          .format(np.average(trans_times),np.std(trans_times)))
    print('translate-remove,  avg: {}\t std dev: {}'
          .format(np.average(remove_times),np.std(remove_times)))


if __name__ == '__main__':
    translate_vs_regex_compare()