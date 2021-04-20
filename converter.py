import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import predictor.utility as util
import datetime


def convertData(df):
    result = pd.DataFrame()
    tarih = df['Tarih']
    date = util.str2date(tarih)
    time = util.date2timestamp(date)
    result['time'] = time
    result['date'] = tarih

    close = util.str2float(df['Şimdi'])
    open = util.str2float(df['Açılış'])
    high = util.str2float(df['Yüksek'])
    low = util.str2float(df['Düşük'])
    #volume = util.str2float(df['Hac.'])

    result['close'] = close
    result['open'] = open
    result['high'] = high
    result['low'] = low
    return result




#only change it
stock_name = 'eregl'
##

if __name__ == "__main__":
    df = pd.read_csv('datas//' + stock_name + '.csv', sep=',')

    df2 = convertData(df)
    df2 = df2.iloc[::-1,:]

    df2.to_csv('datas//' + stock_name + '_conv.csv', sep=',', index=False)

    fig = plt.figure()
    ax = fig.add_subplot(2,1,1)
    ax.plot(df2['time'], df2['close'])


    fig2 = plt.figure()
    ax2 = fig2.add_subplot(1, 1, 1)
    ax2.hist(df2['close'], 100)

    plt.show()

    print(df2.head(20))


