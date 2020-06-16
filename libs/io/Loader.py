import requests

print("downloading with requests")
url = 'http://127.0.0.1:3500/down/db/test.db'
r = requests.get(url)
with open("test.db", "wb") as code:
    code.write(r.content)
