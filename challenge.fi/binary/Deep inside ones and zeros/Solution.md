# Deep inside ones and zeros

## Analyzing

Let's analyze the file
```
$ file level2.out  
level2.out: Mach-O 64-bit x86_64 executable, flags:<NOUNDEFS|DYLDLINK|TWOLEVEL|PIE>
```

This challenge also includes Mach-O binary. This time I directly checked the file with Ghidra and found the same kind of loop as in first binary challenge. 

```c
while (local_48 < 0xb) {
  if ((byte)("ThknsfUrkbt"[local_48] ^ 7U) != local_28[local_48]) {
	bVar1 = true;
  }
  local_48 = local_48 + 1;
}
```

Now this loop goes through string `ThknsfUrkbt` and does [xor](https://en.wikipedia.org/wiki/Exclusive_or) 9 to every character's ord-value

I decoded the string using my python script
```python
en_flag = "OEHNrMljfdy`elE`blHY{ft"
flag = ""
for i in range(len(en_flag)):
  flag+=chr(ord(en_flag[i])^9)

print(f"[+] Flag: {flag}")
```