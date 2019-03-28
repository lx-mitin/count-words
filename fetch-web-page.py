'''Fetch a web page'''
import requests
from bs4 import BeautifulSoup 

# Fetch a web page
p = requests.get('https://github.com/lx-mitin?tab=repositories&q=&type=public')


# Get list of repositories
soup = BeautifulSoup(p.text,'lxml')
reps = soup.body.find_all('a', itemprop="name codeRepository")

for r in reps:
	print('Repository: {} \t address: {}'.format(r.string, r.attrs['href']))