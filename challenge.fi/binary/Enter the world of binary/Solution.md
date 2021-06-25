# Enter the world of binary

## Analyzing

Let's analyze the file to see what we are dealing with.
```
$ file level1.out  
level1.out: Mach-O 64-bit x86_64 executable, flags:<NOUNDEFS|DYLDLINK|TWOLEVEL|PIE>
```

Turns out the file is Mach-o binary and I cannot run it with my linux since it is OS-X compatible. 

## 1st Solve

However, using google I found out that I can run it with [maload](https://github.com/shinh/maloader). 

I ran the binary using maloader and the binary required a password. 
```
$ /opt/maloader/ld-mac.sh ./level1.out  
Thou shall not pass?  
admin  
Thy password: admin  
Thou fool! That is not the answer. Contemplate this on the tree of woe.
```

So I first checked the binary using strings

```
$ strings level1.out
...
Kissa123  
DJ?EyPMRU_qFcpc0.0/{  
Thou shall not pass?  
Thy password: %s  
Thy answer has been accepted! Here is the wisdom for thy benefit.  
Thou fool! That is not the answer. Contemplate this on the tree of woe.
...
```

I tried using `Kissa123` as a password and it worked!
```
$ /opt/maloader/ld-mac.sh ./level1.out  
Thou shall not pass?  
Kissa123  
Thy password: Kissa123  
Thy answer has been accepted! Here is the wisdom for thy benefit.  
FLAG{ROT******}
```

## 2nd Solve

This challenge could be solved without running it by reversing the code. I used Ghidra to read what's inside it. 

While I was looking through the main function I noticed weird loop. 
```c
while (local_44 < 0x14) {
    __stubs::_printf("%c",(ulong)((int)"DJ?EyPMRU_qFcpc0.0/{"[local_44] + 2U),
                     (ulong)((int)"DJ?EyPMRU_qFcpc0.0/{"[local_44] + 2U));
    local_44 = local_44 + 1;
}
```

This loop goes through string `DJ?EyPMRU_qFcpc0.0/{` and takes ord() from the character. Next it adds integer 2 to the ord-value and then returns the character matching that new value. 

I wrote a small script that decodes the string and returns the flag.

```python
en_flag = "DJ?EyPMRU_qFcpc0.0/{"
flag = ""
for i in range(len(en_flag)):
  flag+=chr(ord(en_flag[i])+2)

print(f"[+] Flag: {flag}")
```

