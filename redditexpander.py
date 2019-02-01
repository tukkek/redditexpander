#!/usr/bin/python3
import urllib3,time,json,sys,random

if len(sys.argv)==1:
  raise Exception('Usage: redditexpander.py subreddit [subreddit ...]')

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
  if sub not in SUBS and (sub not in RELATED or score>RELATED[sub]['score']):
    RELATED[sub]={'name':sub,'score':score}
      
def crawl(user):
  user='u/'+user+'/submitted/'
  result=getjson(user)
  if 'data' not in result:
    return
  for post in result['data']['children']:
    post=post['data']
    add(post['subreddit'],post['score'])


def printresults():
  print('Results:')
  html=''
  maxscore=max([x['score'] for x in RELATED.values()])
  if maxscore<1:
    maxscore=1
  for sub in sorted(RELATED.values(),key=lambda x:x['score'],reverse=True):
    name='r/'+sub['name']
    url=PREFIX+name
    score=int(sub['score'])
    score=f' ({round(100*score/maxscore)}%)'
    print('  '+url+score)
    html+=f'<div><a href="{url}" target="_blank">{name+score}</a></div>'''
  print(f'''<html><head><title>reddit expander</title></head>
    <body>{html}</body></html>''',file=open('result.html','w'))

urllib3.disable_warnings()
crawled=set()
random.shuffle(SUBS)
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
