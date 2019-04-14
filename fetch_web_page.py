"""Fetch a web page"""
from requests import get as requests_get
from bs4 import BeautifulSoup 
from json import dump as json_dump
from os import getcwd
from string import punctuation
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk import ne_chunk
from nltk.stem import WordNetLemmatizer

# Define mapping from pos_tag code to lemmatize pos code
def pos_mapping(source_code='NN'):

    mapping = {'JJ':'a','RB':'r','NN':'n','VB':'v','VBD':'v','VBG':'v'}

    try:
        target_code = mapping[source_code]
    except KeyError:
        target_code = 'n'
    
    return target_code

# Fetch a web page
p = requests_get('https://github.com/lx-mitin?tab=repositories&q=&type=public')


# Get a list of repositories
soup = BeautifulSoup(p.text,'lxml')
rep_tags = soup.body.find_all('a', itemprop="name codeRepository")
reps = [{'rep_name':r.string.strip(),
              'rep_url':'https://github.com'+r.attrs['href']} 
            for r in rep_tags]


# Normalize & tokenize text, remove stop words, tag parts of speach,
# tag named entities, reduce words to their root form

translation_dictionaty = {p:' ' for p in punctuation}

for r in reps:
    name = r['rep_name'].casefold()
    name = name.translate(name.maketrans(translation_dictionaty))
    words = word_tokenize(name)
    words = [w for w in words if w not in stopwords.words('english')]
    structure = pos_tag(words)
    structure = ne_chunk(structure)
    r['rep_name'] = [(WordNetLemmatizer().lemmatize(s[0],pos_mapping(s[1])),s[1]) for s in structure]

rep_names = [r['rep_name'] for r in reps]

with open(getcwd()+'/data/rep-names.json','w') as json_file:
    json_dump(rep_names,json_file)

    
print('Repositories list is loaded to `/data/rep-names.json` file')
