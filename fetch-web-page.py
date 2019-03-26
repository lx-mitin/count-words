'''Fetch a web page'''
import requests
import re

# Fetch a web page
p = requests.get('https://github.com/lx-mitin?tab=repositories&q=&type=public')


# Remove HTML tags using RegEx
pattern = re.compile(r'<.*?>')
t = pattern.sub('',p.text)

print(t)