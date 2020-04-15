#!/usr/bin/python3
import urllib3,time,json,sys,random

if len(sys.argv)==1:
  raise Exception('Usage: redditexpander.py subreddit [subreddit ...]')

DEBUG=False
PREFIX='http://www.reddit.com/'
SUBS=set(sub.lower().replace('r/','').replace('/','') for sub in sys.argv[1:])
HTTP=urllib3.PoolManager()
FOUND=set(SUBS)

html=''

def get(url):
  try:
    print(url)
    return HTTP.request('GET',url).data
  finally:
    if not DEBUG:
      time.sleep(3)
      
def getjson(url):
  return json.loads(get(PREFIX+url+'/.json'))
      
def crawl(user):
  user='u/'+user+'/submitted/'
  result=getjson(user)
  if 'data' in result:
    addresults(post['data'] for post in result['data']['children'])

def addresults(r):
  global html
  global FOUND
  separate=False
  for sub in sorted(r,key=lambda x:x['subreddit_subscribers'],reverse=True):
    name=sub['subreddit'].lower()
    '''if len(FOUND)>0:
      print(name)
      print(list(FOUND)[0])
      print(list(SUBS)[0])'''
    if name not in FOUND:
      FOUND.add(name)
      a=f'<a href="{PREFIX}r/{name}" target="_blank">{sub["subreddit"]} ({sub["subreddit_subscribers"]:,})</a>'
      html+=f'<div>{a}</div>'
      separate=True
  if separate:
    html+='<hr/>'

def printresults():
  style='<style>div{margin:.5em;display:inline-block;}</style>'
  print(f'''<html><head><title>reddit expander</title>{style}</head>
    <body>{html}</body></html>''',file=open('result.html','w'))

print(f'Processing: {" ".join(SUBS)}')
urllib3.disable_warnings()
users=set()
for sub in SUBS:
  for post in getjson(f'r/{sub}')['data']['children']:
    user=post['data']['author']
    if not user in users:
      users.add(user)
      crawl(user)
      printresults()
      if DEBUG:
        break
  if DEBUG:
    break
printresults()
