"""Count words"""
import string
from collections import defaultdict

def count_words(text):

    t = text.casefold()    
    t = t.translate(t.maketrans('','', string.punctuation))
    t = t.split()
    
    cw = defaultdict(int)
    for w in t:
        cw[w] += 1

    return cw

def test_run():
    from datetime import datetime 
    with open('./texts/roadside-picnic-ru.txt','r') as f:
        t = f.read()
        print('Start counting time: {}'.format(datetime.now()))
        words = count_words(t)
        print('End counting time: {}'.format(datetime.now()))
        
        print('Total number of words: {}'.format(sum(words.values())))
        print('Number of unique words: {}'.format(len(words)))
        
        sorted_counts = sorted(words.items(), key=lambda p:p[1], reverse=True)
        print('10 most popular words are:')
        for word, count in sorted_counts[:10]:
            print('{}:\t{}'.format(word, count))

if __name__ == '__main__':
    test_run()
