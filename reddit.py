import praw
import pandas as pd
import datetime as dt

reddit = praw.Reddit(client_id='G7PaAUWsihKXw5BqwpbiBA', \
                     client_secret='7BuTLAkCWVWHgG5CyU3rDNXTeolS_g', \
                     user_agent='7BuTLAkCWVWHgG5CyU3rDNXTeolS_g', \
                     username='DeskExternal6897', \
                     password='Hv9Tw:nJzJ!9zWF')

subreddits = ['bitcoin', 'crypto', 'cryptocurrency', 'bitcoinbeginner'] #, 'litecoin', 'dogecoin', 'ethtrader', 'ethereum', 'shibarmy']

def get_date(created):
    return dt.datetime.fromtimestamp(created)

def get_reddit_data_by_sub_limit(sub, limit=1000):
    subreddit = reddit.subreddit(sub)
    new_subreddit = subreddit.new(limit=limit)
    
#    df_rows = [[sub, submission.id, submission.author.id, submission.author.name, submission.author.comment_karma + submission.author.link_karma, submission.title, submission.score, submission.upvote_ratio, submission.num_comments, submission.created, submission.selftext] for submission in new_subreddit]
#    df = pd.DataFrame(df_rows, columns=['subreddit', 'id', 'author_id', 'author_name', 'author_karma', 'title', 'score', 'upvote_ratio', 'comms_num', 'created', 'body'])

    df_rows = [[sub, submission.id, submission.title + ' ' + submission.selftext, submission.score, submission.upvote_ratio, submission.num_comments, submission.created] for submission in new_subreddit]
    df = pd.DataFrame(df_rows, columns=['subreddit', 'id', 'text', 'score', 'upvote_ratio', 'comms_num', 'created'])

    df = pd.DataFrame(df)
    _timestamp = df["created"].apply(get_date)
    df = df.assign(date = _timestamp)
    return df
    
combDF = []

for x in subreddits:
    print(x)
    
    df = get_reddit_data_by_sub_limit(x)
    combDF.append(df)

combDF = pd.concat(combDF)
combDF.to_csv('reddit.csv', index=False)