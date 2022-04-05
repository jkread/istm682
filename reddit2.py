import requests
import praw
from psaw import PushshiftAPI
import pandas as pd
import datetime as dt
import time

subreddits = ['bitcoin', 'crypto', 'cryptocurrency', 'bitcoinbeginners']
date = dt.datetime(2021, 12, 1, 0, 0)
limit = 365
datestart = int((date - dt.timedelta(limit)).timestamp())
date = int(date.timestamp())

def subreddit_historical(subreddit, date, startdate):
    fields = 'id,created_utc,title,selftext,score,upvote_ratio,comms_num'
    url = 'https://api.pushshift.io/reddit/submission/search?subreddit={}&fields={}&limit=100&before={}'.format(subreddit, fields, date)
    subs = []
    x = 0
    while True:
        x += 1
        turl = url + '&after={}'.format(startdate)
        print(turl)
        print(x)
        page = requests.get(turl)
        data = page.json()['data']
        df = pd.DataFrame(data)
        startdate = data[-1]['created_utc']+1
        subs.append(df)
        df['timestamp'] = [dt.datetime.fromtimestamp(d) for d in df.created_utc]
        if len(data) < 100:
            break
        time.sleep(1.1)
    subs = pd.concat(subs)
    subs['subreddit'] = subreddit
    return subs

combDF = []

for x in subreddits:
    print(x)
    df = subreddit_historical(x, date, datestart)
    combDF.append(df)

combDF = pd.concat(combDF)
combDF.to_csv('reddit2.csv', index=False)


    
