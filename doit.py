from pwn import *

def connect(): return remote("0", 1337, level="error")

def hasher(data):
    r = connect()
    if data: r.send(data)
    r.shutdown()
    resp = r.recvall().decode().strip()
    r.close()
    return resp

p = log.progress("Flag")

last_hsh = None
for i in reversed(range(128)):
    p.status(f"Finding length {i}")
    hsh = hasher(b"\x00"*i)
    if last_hsh and last_hsh != hsh: break
    last_hsh = hsh

flag = b""

while i > len("This is the flag:"):
    correct = hasher(b"\x00"*i)
    if i == 0: break
    for b in string.printable.encode():
        test_flag = bytes([b]) + flag
        p.status(f"Bruteforcing {test_flag}")
        test = hasher(b"\x00"*i + test_flag)
        if test == correct: break
    flag = test_flag
    i -= 1

p.success(flag.decode().strip())
