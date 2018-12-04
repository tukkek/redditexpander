#!/usr/bin/python3
import urllib3,time,json,sys

DEBUG=False
PREFIX='http://www.reddit.com/'
SUBS=sys.argv[1:]
HTTP=urllib3.PoolManager()
RELATED={}

def get(url):
  try:
    print(url)
    return HTTP.request('GET',url).data
  finally:
    if not DEBUG:
      time.sleep(3)
      
def getjson(url):
  return json.loads(get(PREFIX+url+'/.json'))
      
def add(sub,score):
  if sub in SUBS:
    return
  if sub not in RELATED or score>RELATED[sub]['score']:
    RELATED[sub]={'name':sub,'score':score}
      
def crawl(user):
  user='u/'+user+'/submitted/'
  for post in getjson(user)['data']['children']:
    post=post['data']
    add(post['subreddit'],post['score'])

def printresults():
  print('Results:')
  for sub in sorted(RELATED.values(),key=lambda x:x['score'],reverse=True):
    print('  '+PREFIX+'r/'+sub['name']+' '+str(sub['score']))

urllib3.disable_warnings()
crawled=set()
for sub in SUBS:
  for post in getjson('r/'+sub)['data']['children']:
    user=post['data']['author']
    if not user in crawled:
      crawled.add(user)
      crawl(user)
      printresults()
      if DEBUG:
        break
  if DEBUG:
    break
printresults()
