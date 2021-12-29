# ret2the-unknown

The file takes input with `gets()` and it allows us to buffer overflow. Since we are given a libc file with the binary, I assumed this was going to be a return-2-libc. There was nothing special about this attack since protections were only NX.

## Exploitation

### Part 1.
1. Leaks puts-address in LIBC
2. Leak LIBc-base-address using leaked puts.
3. Call Main-function to continue the flow.

### Part 2.
1. Align the stack
2. Set `/bin/sh` into RDI
3. Execute system()

### Flag
flag{rob-is-proud-of-me-for-exploring-the-unknown-but-i-still-cant-afford-housing}
