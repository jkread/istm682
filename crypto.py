import requests
import datetime
import pandas as pd
import datetime as dt

symbols = ['BTC'] #, 'ETH', 'DOGE', 'LTC', 'SHIB']
date = dt.datetime(2021, 12, 1, 0, 0).timestamp()
limit = 1

def daily_price_historical(symbol, comparison_symbol='USD', all_data=False, limit=1, aggregate=1, exchange='', ts=0):
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate={}'.format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    if all_data:
        url += '&allData=true'
    if ts:
        url += '&toTs={}'.format(ts)
    print(url)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df

def get_dataframe_by_symbol_limit(symbol, limit=365, ts=0):
    df = daily_price_historical(symbol, limit=limit, ts=ts)
    df['Symbol'] = symbol
    return df

combDF = []

print('Gathering...')
for x in symbols:
    print(x)
    df = get_dataframe_by_symbol_limit(x, limit, date)
    combDF.append(df)

print('Exporting...')
combDF = pd.concat(combDF)
combDF.drop(['conversionType', 'conversionSymbol'], 1 , inplace=True)
combDF.to_csv('crypto.csv', index=False)
print('Done')



