import pandas as pd
import random
import os
import nltk
nltk.downloader.download('vader_lexicon')
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

print('Reading in files')
df2 = []

for file in os.scandir('data/posts'):
   df2.append(pd.read_csv(file.path))

df2 = pd.concat(df2)
df2['text'] = df2['title'].astype(str) + ' ' + df2['selftext'].astype(str)
df2.to_csv('data/compiled.csv', index=False)
print('Output')
    
