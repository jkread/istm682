import requests
import pandas as pd
import datetime as dt
import time

#subreddits = ['bitcoin', 'crypto', 'cryptocurrency', 'bitcoinbeginners']
subreddits = ['bitcoin']
date = dt.datetime(2021, 12, 1, 0, 0)
limit = 1
datestart = int((date - dt.timedelta(limit)).timestamp())
date = int(date.timestamp())
posts = True
comments = False

def pushshift_query(url, startdate):
    rslt = []
    x = 0
    y = 0
    while True:
        x += 1
        turl = url + '&after={}'.format(startdate)
        print('------------------------------------------------')
        print('Iteration #' + str(x))
        print(turl)
        page = requests.get(turl)
        if page.status_code != 200:
            print('Error')
            break
        data = page.json()['data']
        if data == []:
            print('Empty Result')
            break
        y += len(data)
        print(str(len(data)) + ' new records, ' + str(y) + ' total records')
        df = pd.DataFrame(data)
        startdate = data[-1]['created_utc']+1
        rslt.append(df)
        time.sleep(1.1)
    rslt = pd.concat(rslt)
    rslt['timestamp'] = [dt.datetime.fromtimestamp(d) for d in rslt.created_utc]
    return rslt
    
def subreddit_historical(subreddit, date, startdate):
    fields = 'id,created_utc,title,selftext,score,upvote_ratio,num_comments,subreddit,total_awards_received'
    url = 'https://api.pushshift.io/reddit/submission/search?subreddit={}&fields={}&limit=100&before={}'
    url = url.format(subreddit, fields, date)
    return pushshift_query(url, startdate)

def comment_historical(subreddit, date, startdate):
    fields = 'id,parent_id,created_utc,author,body,score,subreddit,total_awards_received'
    url = 'https://api.pushshift.io/reddit/comment/search?subreddit={}&fields={}&limit=100&before={}'
    url = url.format(subreddit, fields, date)
    return pushshift_query(url, startdate)

combDF = []

for x in subreddits:
    if posts:
        print(x)
        print('Posts')
        df = subreddit_historical(x, date, datestart)
        size = len(df)
        filename = './data/posts/' + x + '_posts_' + str(datestart) + '_' + str(date) + '_' + str(size) + '.csv'
        df.to_csv(filename, index=False)
    if comments:
        print('Comments')
        df = comment_historical(x, date, datestart)
        size = len(df)
        filename = './data/comments/' + x + '_comments_' + str(datestart) + '_' + str(date) + '_' + str(size) + '.csv'
        df.to_csv(filename, index=False)
print('Done')



    
