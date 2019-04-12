"""Compare translate vs regex for text normalization task"""
from string import punctuation
from re import sub
from datetime import datetime
import numpy as np
from os import walk

# replace punctuation characters with space by using regular expression
def normalize_regex(text):
    
    return sub(r'[^a-zA-Zа-яА-Я0-9]',' ',text)

# replace punctuation characters with space by using regular expression 
# (letter are preliminary lowered)
def lower_regex(text):
    
    return sub(r'[^a-zа-я0-9]',' ',text)

# replace punctuation characters with space by using translate
def normalize_trans(text):

    translation_dictionary = {p:' ' for p in punctuation}
    return text.translate(text.maketrans(translation_dictionary))

# remove punctuation characters by using translate
def remove_punctuation_translate(text):
    return text.translate(text.maketrans('','',punctuation))


#  compare translate vs regex
def translate_vs_regex_compare():

    results = []
    for root, dirs, files in walk('./data-txt'):

        for filename in files:

            result = {}
            result['name'] = filename

            with open(root+'/'+filename,'r') as f:

                text = f.read()
            
            result['length'] = len(text)

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

            result['regex_times'] = regex_times
            result['lower_times'] = lower_times
            result['trans_times'] = trans_times
            result['remove_times'] = remove_times

            result['regex_avg'] = np.average(regex_times)
            result['lower_avg'] = np.average(lower_times)
            result['trans_avg'] = np.average(trans_times)
            result['remove_avg'] = np.average(remove_times)

            result['regex_std'] = np.std(regex_times)
            result['lower_std'] = np.std(lower_times)
            result['trans_std'] = np.std(trans_times)
            result['remove_std'] = np.std(remove_times)

            results.append(result)

    for r in results:
        print('name: {},\tlength: {},\tregex: {},\ttranslate: {}'
              .format(r['name'],r['length'],r['regex_avg'],r['trans_avg']))

if __name__ == '__main__':
    translate_vs_regex_compare()