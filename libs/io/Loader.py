import requests

print("downloading with requests")
# url = 'http://127.0.0.1:3500/down/db/ccs.db'
url = 'http://192.168.9.54:3500/load/down/db/ccs.db'
r = requests.get(url)
with open("copy_css.db", "wb") as code:
    code.write(r.content)
