'''Fetch a web page'''
import requests
from bs4 import BeautifulSoup 

# Fetch a web page
p = requests.get('https://github.com/lx-mitin?tab=repositories&q=&type=public')


# Remove HTML tags using BeatifulSoup library
soup = BeautifulSoup(p.text)
t = soup.get_text()

print(t)