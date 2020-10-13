import requests
from bs4 import BeautifulSoup

r = requests.get("https://2019shell1.picoctf.com/problem/37886/")
# print(r.text)
soup = BeautifulSoup(r.text, 'html.parser')
script = soup.findAll("script")[1].string

# The list 'vars' stores different parts of the password
vars = script.split(";")[0].split("=[")[1].split("','")
for i in range(len(vars)):
    vars[i] = vars[i].strip("']")

# rotate the list 'vars'
while vars[0] != "getElementById":
    vars.insert(0, vars.pop())

# split the verify function string to parse more easily
verify = script.split(";")[11].split("){")
verify = verify[0:len(verify)-1]

indexes = []
parts = []
for v in verify:
    index, part = v.split("==")
    index = index.split("]")[1]
    indexes.append(index)
    parts.append(part)

# process the index
for i in range(len(indexes)):
    index = indexes[i]
    if index == '(0x0,split*0x2)':
        index = (0, 8)
    elif index=='(0x7,0x9)':
        index = (7, 9)
    elif index == "(split*0x2,split*0x2*0x2)":
        index = (8, 16)
    elif index == "(0x3,0x6)":
        index = (3, 6)
    elif index == "(split*0x3*0x2,split*0x4*0x2)":
        index = (24, 32)
    elif index == "(0x6,0xb)":
        index = (6, 11)
    elif index == "(split*0x2*0x2,split*0x3*0x2)":
        index = (16, 24)
    elif index == "(0xc,0x10)":
        index = (12, 16)
    indexes[i] = index

# process the different parts of the password
for i in range(len(parts)):
    part = parts[i]
    if "_0x4b5b" in part:
        index = part[11]
        part = vars[int(index)]
    part = part.strip("'")
    parts[i] = part

# print(indexes)
# print(parts)

password = " "*32
for i in range(len(indexes)):
    start, end = indexes[i]
    password = password[:start] + parts[i] + password[end:]
# print(password)

flag = password[password.index("{")+1: len(password)-1]
print(flag)







