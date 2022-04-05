import pandas as pd
import random
import os
import nltk
nltk.downloader.download('vader_lexicon')
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

weights = [['positive', 0.5], ['neutral', 0.1], ['negative', -0.1]]



def determine_sentiment(text):
    # adding crypto reddit to vader to improve sentiment analysis, score: 4.0 to -4.0. Rank each keyword
    new_words = {
        'lambo': 4.0,
        'rekt': -4.0,
        'citron': -4.0,
        'hidenburg': -4.0,
        'moon': 4.0,
        'Elon': 2.0,
        'hodl': 2.0,
        'highs': 2.0,
        'mooning': 4.0,
        'long': 2.0,
        'short': -2.0,
        'call': 4.0,
        'calls': 4.0,
        'put': -4.0,
        'puts': -4.0,
        'break': 2.0,
        'tendie': 2.0,
        'tendies': 2.0,
        'town': 2.0,
        'overvalued': -3.0,
        'undervalued': 3.0,
        'buy': 4.0,
        'sell': -4.0,
        'gone': -1.0,
        'gtfo': -1.7,
        'fomo': 2.0,
        'paper': -1.7,
        'bullish': 3.7,
        'bearish': -3.7,
        'bagholder': -1.7,
        'stonk': 1.9,
        'green': 1.9,
        'money': 1.2,
        'print': 2.2,
        'rocket': 2.2,
        'bull': 2.9,
        'bear': -2.9,
        'pumping': 1.0,
        'sus': -3.0,
        'offering': -2.3,
        'rip': -4.0,
        'downgrade': -3.0,
        'upgrade': 3.0,
        'maintain': 1.0,
        'pump': 1.9,
        'hot': 2,
        'drop': -2.5,
        'rebound': 1.5,
        'crack': 2.5, }

    vader = SentimentIntensityAnalyzer()
    #Adding custom words to Vader
    vader.lexicon.update(new_words)
    print(text)
    scores = vader.polarity_scores(text)
    print('.', end='')
    return scores
    
def determine_impact(df):
    sent = determine_sentiment(df['text'])
    wght = (df['num_comments'] + df['score']) * df['upvote_ratio']
    return sent*wght

def printmr(text):
    print(text)
    return len(text)

#df = pd.read_csv('crypto.csv')
#print(df)

print('Reading in files')
df2 = []

for file in os.scandir('data/posts'):
   df2.append(pd.read_csv(file.path))

df2 = pd.concat(df2)
print('Analyzing')
df2['text'] = str(df2['title'] + ' ' + df2['selftext'])
df2['sentiment'] = printmr(df2['text'])
#df2 = df2[['created_utc', 'impact']]
df2.to_csv('data/reddit_analyzed.csv', index=False)
print('Output')