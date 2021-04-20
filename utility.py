import numpy as np
import pandas as pd
import datetime

def str2float(text):
    if type(text)==str:
        return float(text.replace('.', '').replace(',', '.'))
    elif type(text)==list or type(text)==pd.core.series.Series:
        result = []
        for a in text:
            result.append(str2float(a))
        return result
    else:
        print('convertion type is not supported!')
        return None


def str2date(text, is_intraday=False):
    if type(text) == str:
        if is_intraday:
            date = datetime.datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
        else:
            date = datetime.datetime.strptime(text, "%d.%m.%Y")
        #.strftime("%d.%m.%Y")
        return date

    elif type(text) == list or type(text)==pd.core.series.Series:
        result = []
        for a in text:
            result.append(str2date(a, is_intraday))
        return result
    else:
        print('convertion type is not supported!')
        return None


def date2timestamp(date):
    if type(date) == datetime.datetime:
        return date.timestamp()
    elif type(date) == list or type(date)==pd.core.series.Series:
        result = []
        for a in date:
             result.append(date2timestamp(a))
        return result
    else:
        print('convertion type is not supported!')
        return None


def map(x, num=1):
    df = pd.DataFrame()
    for i in range(num):
        df['x'+str(i+1)] = exp(x,i+1)
    return df

def exp(x, num):
    if type(x) == list or type(x) == pd.core.series.Series:
        result = []
        for a in x:
            result.append(exp(a,num))
        return result
    else:
        return x**num

