import requests
from bs4 import BeautifulSoup
r = requests.get("https://2019shell1.picoctf.com/problem/37829/flag", headers={"User-Agent": "picobrowser"})
soup = BeautifulSoup(r.text, 'html.parser')
flag = soup.code.text
# print(flag)
print(soup.code.text[8:len(soup.code.text)-1])


