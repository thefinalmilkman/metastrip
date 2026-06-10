import urllib.request, json
KEY='jXjwU85JeJ9wz6EeyJ6JCUwr'
body=open('devto-article.md',encoding='utf-8').read()
payload={"article":{
  "title":"Your photos are quietly leaking your home address — the byte-level reason, and a fix",
  "published":True,
  "body_markdown":body,
  "tags":["privacy","security","javascript","webdev"],
  "description":"Every JPEG carries the exact GPS coordinates where it was taken. Here's how EXIF stores it, why cropping doesn't remove it, and how to strip it losslessly — with a 100% in-browser tool."
}}
data=json.dumps(payload).encode()
req=urllib.request.Request("https://dev.to/api/articles",data=data,method="POST",
  headers={"api-key":KEY,"Content-Type":"application/json","User-Agent":"metastrip-publish"})
try:
    r=urllib.request.urlopen(req,timeout=45)
    j=json.load(r)
    print("PUBLISHED:",j.get("url"))
except urllib.error.HTTPError as e:
    print("HTTP",e.code,e.read().decode()[:500])
except Exception as e:
    print("ERR",repr(e))
