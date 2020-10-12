import requests
from bs4 import BeautifulSoup

r = requests.get("https://2019shell1.picoctf.com/problem/37886/")
# print(r.text)
soup = BeautifulSoup(r.text, 'html.parser')
script = soup.findAll("script")[1].string
print(script)

