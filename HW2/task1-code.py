import requests
from bs4 import BeautifulSoup

# helper function
def find_digit(string):
    for c in string:
        if c.isdigit():
            return c
    return '-1'

r = requests.get("https://2019shell1.picoctf.com/problem/49886/")
# print(r.text)
soup = BeautifulSoup(r.text, 'html.parser')
script = soup.findAll("script")[1].string
lines = script.splitlines()
lines = [line.strip() for line in lines]
# print(lines)

parts = {}
for line in lines:
    if "substring" in line:
        index, part = line.split(" == ")
        index = index.split(", ")[1]
        part = part.strip("'").split("') ")[0]
        # print(index)
        # print(part)
        if find_digit(index) == '-1':
            index = '1'
        else:
            index = find_digit(index)
        parts[index] = part
# print(parts)

password = ""
for i in range(1, 9):
    password+=parts[str(i)]
# print(password)

flag = password[password.index("{")+1: len(password)-1]
print(flag)








