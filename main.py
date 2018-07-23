import requests
import json
import ast
import pandas as pd

def get_symbols():
   r = requests.get('https://api.iextrading.com/1.0/ref-data/symbols')
   json_file = json.loads(r.text)
   symbols = [j['symbol'].lower() for j in json_file]
   return symbols

def prepare(content):
    df = pd.DataFrame(ast.literal_eval(content))
    df['ticker'] = company.upper()
    df['date'] = pd.to_datetime(df['date'])
    df = df.loc[df['date'] >= begin]
    df = df.loc[df['date'] <= end]
    df['week_high'] = df['high'].rolling(window=5).max()
    df['week_low'] = df['low'].rolling(window=5).min()
    df['week_open'] = df['open'].shift(4)
    df['week_close'] = df['close']
    df['week_change'] = df['close'] - df['close'].shift(5)
    df['week_change'] = df['week_change'].apply(lambda x: round(x, 2))
    df = df[['ticker', 'date', 'week_high', 'week_low', 'week_open', 'week_close', 'week_change']]
    df = df.loc[df['date'] == end]
    return df
if __name__=="__main__":
    end = '2008-05-25'
    begin = '2018-05-18'
    company_list = get_symbols()
    re = []
    for company in company_list:
        try:
            content = requests.get('https://api.iextrading.com/1.0/stock/'+company+'/chart/1m')
            df = prepare(content.text)
            dict_temp = df.to_dict('records')
            re.append(dict_temp[0])
        except:
            continue
    res = pd.DataFrame(re)
    res.to_csv('../datasets/data.csv',index=False)
