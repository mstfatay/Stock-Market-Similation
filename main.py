import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import predictor.utility as util
import predictor.simulation as simulation
import datetime
import ta
from ta import volatility
from ta import trend



#makes everything initialized
##########################

stock_name = 'thyao'
leverage = 1


df = pd.read_csv('datas//' + stock_name + '_conv.csv', sep=',')
tarih = df['date']
df['date'] = util.str2date(tarih, False)

#df['close'] = 132613.81 + 18128.33 - df['close']
#df['open'] = 132613.81 + 18128.33 - df['open']
#df['high'] = 132613.81 + 18128.33 - df['high']
#df['low'] = 132613.81 + 18128.33 - df['low']

# Clean NaN values
#df = ta.utils.dropna(df)

print(type(df['open'].iloc[2]))
print(type(df['close'].iloc[2]))
print(type(df['high'].iloc[2]))
print(type(df['low'].iloc[2]))


df = ta.add_all_ta_features(df, open="open", high="high", low="low", close="close", volume="low")

#########################

'''
indicator_bb  = volatility.BollingerBands(close=df["close"], n=100, ndev=2)


mid_band = indicator_bb.bollinger_mavg()
high_band = indicator_bb.bollinger_hband()
low_band = indicator_bb.bollinger_lband()
print(mid_band.head(20))
'''

#macd
###########################

#for ibm
#1d   26,12,9
#5min 13,6,3
#1min 26,13,9  bettersim(0.00025)

ind_macd = trend.MACD(close=df['close'], n_slow=26, n_fast=13, n_sign=9)
macd = ind_macd.macd()
signal = ind_macd.macd_signal()
diff = ind_macd.macd_diff()


#print(macd.head(10))
#print(signal.head(10))
#print(diff.head(10))


#simulation
############################


sim = simulation.BasicSim(df, macd, signal, diff, 'better_sim',num_of_sub=10,
                          start=0, end=-1, sort_enabled=False, leverage=leverage)
sim.determineOperations()
sim.saveOperations()
sim.save()
sim.gainAnalysis( plot = False)
sim.findAnualGainRatios()


start_date = datetime.datetime(2000,1,1)
end_date = datetime.datetime(2021,1,1)

sim.print(True, start_date, end_date)
sim.gainAnalysis(True, start_date=start_date, end_date=end_date)
#sim.detailedAnalysis()

#sim.plot()


#plot
############################
'''
fig, (sub1, sub2) = plt.subplots(2,1)
sub1.plot(df['date'], df['close'], 'b')
sub2.plot(df['date'], macd, 'b')
sub2.plot(df['date'], signal, 'r')
sub2.plot(df['date'], diff, 'g')
plt.show()

#print(df.columns)

'''