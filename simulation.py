import predictor.utility as util
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.max_rows", None)

class Simulation():
    #df
    #bought
    #sold
    #money
    #gain_ratio     not percent
    #gain
    #paid
    #path
    #name

    #macd
    #signal
    #diff

    #operations
    #moves
    #last_df

    #time_list = []
    #sub_size
    #num_of_sub

    #sort_enabled
    #leverage
    #bankrupted

    def __init__(self, df, macd=None, signal=None, diff=None, path = 'datas', fromDisk = False,
                 num_of_sub = 1, start=0, end=-1, sort_enabled = False, leverage=1):
        if fromDisk==True:
            pass
        else:
            self.macd = macd
            self.signal = signal
            self.diff = diff
        self.df = df
        self.name = 'Simulation'
        self.bought = False
        self.sold = False
        self.money = 17128
        self.gain = 0
        self.gain_ratio = 0
        self.path = path
        self.operations = pd.DataFrame()
        self.moves = pd.DataFrame(columns=['time','date','buy','sell','price','gain_ratio'])
        self.sort_enabled = sort_enabled
        self.leverage = leverage
        self.bankrupted = False

        if end == -1:
            finish = self.df.shape[0]
        else:
            finish = end
        self.num_of_sub = num_of_sub
        self.sub_size = int((finish-start)/num_of_sub)
        self.time_list = []
        tmp = start
        for i in range(num_of_sub):
            self.time_list.append(self.df['time'].iloc[tmp+i*self.sub_size])
        self.time_list.append(self.df['time'].iloc[end])


    def determineOperations(self):
        buy, sell = self._determineBuySell()
        diction = {'buy': buy, 'sell': sell}
        self.operations = pd.DataFrame(diction)
        self.operations['date'] = self.df['date']
        self.operations['time'] = self.df['time']

    def _determineBuySell(self):
        pass

    def _buy(self, index):
        if not self.bought:
            if index >= self.df.shape[0]:
                return
            value = self.df['open'].iloc[index]
            date = self.df['date'].iloc[index]
            time = self.df['time'].iloc[index]
            self.bought = True
            gain_ratio = 0.0
            if self.sort_enabled and self.sold:
                g = (1 - value / self.paid) * self.leverage
                self.money *= g + 1
                self.gain_ratio += g
                self.sold = False
                gain_ratio = g
            self.paid = value
            self._addMove(time,date,True,False,value,gain_ratio)


    def _sell(self, index):
        if self.bought:
            if index >= self.df.shape[0]:
                return
            value = self.df['open'].iloc[index]
            date = self.df['date'].iloc[index]
            time = self.df['time'].iloc[index]
            g = (value / self.paid - 1) * self.leverage
            if g < -1:
                g = -1
                self.bankrupted = True
            self.money *= g + 1
            self.gain_ratio += g
            self.bought = False
            if self.sort_enabled:
                self.paid = value
                self.sold = True
            self._addMove(time, date, False, True, value, g)

    def _addMove(self, time, date, buy, sell, price, gain_ratio = np.nan):
        dic = {'time': [time], 'date': [date], 'buy': [buy], 'sell': [sell], 'price': [price],
               'gain_ratio': [gain_ratio]}
        added = pd.DataFrame(dic)
        self.moves = self.moves.append(added, ignore_index=True)

    def saveOperations(self):
        print(self.path)
        self.operations.to_csv(self.path +'//operations.csv', index=False)

    def save(self):
        macd_df = pd.DataFrame()
        macd_df['time'] = self.df['time']
        macd_df['date'] = self.df['date']
        macd_df['macd'] = self.macd
        macd_df['signal'] = self.signal
        macd_df['diff'] = self.diff

        macd_df.to_csv(self.path +'//macd_df.csv', index=False)
        self.moves.to_csv(self.path +'//moves_df.csv', index=False)

###########################

    def gainAnalysis(self, use_last_df = False, start_date=None, end_date = None, plot=True):
        if use_last_df:
            orders = self.last_df
        else:
            if self.sort_enabled:
                orders = self.moves
            else:
                orders = self.moves[self.moves['sell'] == True]
        if start_date != None:
            start_time = start_date.timestamp()
            end_time = end_date.timestamp()
            orders = orders[(orders['time']>=start_time) & (orders['time']<end_time)]

        gains = orders[orders['gain_ratio']>0]
        losses = orders[orders['gain_ratio'] < 0]

        gain_loss_analysis = orders['gain_ratio'].describe()
        gains_analysis = gains['gain_ratio'].describe()
        losses_analysis = losses['gain_ratio'].describe()

        print('gains/losses anaylsis')
        print(gain_loss_analysis)
        print('gains anaylsis')
        print(gains_analysis)
        print('losses anaylsis')
        print(losses_analysis)

        if plot == True:
            self.plotGains(use_last_df=use_last_df)


    # performance issues: orders is created 2 times!
    def detailedAnalysis(self):
        print('---------------------------------')
        for i in range(self.num_of_sub):
            date = datetime.datetime.fromtimestamp(self.time_list[i])
            date2 = datetime.datetime.fromtimestamp(self.time_list[i + 1])
            print("Analysis: (" + str(date) + ')' )
            self.printGainRatio(date, date2)
            self.gainAnalysis(True, date, date2)
            print()
        self.plotGains()
        print('---------------------------------')


    def findAnualGainRatios(self, start=2000, end=2020, step=1):
        result = pd.DataFrame(columns=['time','date','open','close','base_gain_ratio','gain_ratio'])
        for i in range(self.num_of_sub):
            date = datetime.datetime.fromtimestamp(self.time_list[i])
            date2 = datetime.datetime.fromtimestamp(self.time_list[i+1])
            tmp = self._findAnCompositeGainRatio(date,date2)
            result = result.append(tmp, ignore_index=True)
            #self.printGainRatio(date, date2)
            #self.gainAnalysis(date, date2)
        self.last_df = result
        print(result)

    def _findAnCompositeGainRatio(self, start_date, end_date, use_last_df = False,):
        if use_last_df:
            orders = self.last_df
        else:
            if self.sort_enabled:
                orders = self.moves
            else:
                orders = self.moves[self.moves['sell'] == True]
        start_time = start_date.timestamp()
        end_time = end_date.timestamp()
        orders = orders[(orders['time'] >= start_time) & (orders['time'] < end_time)]

        mult = 1
        for a in orders['gain_ratio']:
            mult *= a + 1
        gain_ratio = mult
        open = self.df[self.df['time']>=start_time]['close'].iloc[0]
        close = self.df[self.df['time'] < end_time]['close'].iloc[-1]
        base_gain_ratio = close/open
        dic = {'time':[start_time], 'date':[start_date], 'open':[open], 'close':[close], 'base_gain_ratio':base_gain_ratio-1, 'gain_ratio':[gain_ratio-1]}
        result = pd.DataFrame(dic)
        return result


    def printGainRatio(self, start_date, end_date):
        if self.sort_enabled:
            orders = self.moves
        else:
            orders = self.moves[self.moves['sell'] == True]
        start_time = start_date.timestamp()
        end_time = end_date.timestamp()
        orders = orders[(orders['time'] >= start_time) & (orders['time'] < end_time)]

        print(orders)

        print("gain's sum: " + str(orders['gain_ratio'].sum()))
        mult = 1
        for a in orders['gain_ratio']:
            mult *= a+1
        print('composite gain rate: ' + str(mult))
        print('percent: ' + str(mult*100) + '%')



    def plotGains(self, use_last_df = False):
        fig = plt.figure()
        fig.suptitle(self.name + " object's figure")
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.set_title('close prices and buy/sell points')
        ax2 = fig.add_subplot(2, 1, 2)
        ax2.set_title('gain ratios of sells')

        orders = self.moves[self.moves['sell']==True]
        ax2.stem(orders['date'], orders['gain_ratio'])

        buys = self.moves[self.moves['buy'] == True]
        sells = self.moves[self.moves['sell'] == True]

        ax1.plot(self.df['date'], self.df['close'], 'b')
        ax1.plot(buys['date'], buys['price'], 'gx')
        ax1.plot(sells['date'], sells['price'], 'rx')

        fig2 = plt.figure()
        fig2.suptitle(self.name + " object's figure")
        ax3 = fig2.add_subplot(1,1,1)
        ax3.set_title("gain ratio's histagram")

        if use_last_df:
            ax3.hist(self.last_df['gain_ratio'], 20)
        else:
            ax3.hist(orders['gain_ratio'],20)

        plt.show()


    def plot(self):
        fig = plt.figure()
        fig.suptitle(self.name + " object's figure")
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.set_title('close prices')
        ax2 = fig.add_subplot(2, 1, 2)
        ax2.set_title('macd')

        ax1.plot(self.df['date'], self.df['close'], 'b')
        ax2.plot(self.df['date'], self.macd, 'b')
        ax2.plot(self.df['date'], self.signal, 'r')
        ax2.stem(self.df['date'], self.diff, bottom=0, use_line_collection=True)

        buys = self.moves[self.moves['buy'] == True]
        sells = self.moves[self.moves['sell'] == True]

        ax1.plot(buys['date'], buys['price'], 'gx')
        ax1.plot(sells['date'], sells['price'], 'rx')

        plt.show()


    def print(self, use_last_df=False, start_date=None, end_date=None):
        #print(self.operations)
        if use_last_df:
            k = self._findAnCompositeGainRatio(start_date,end_date, use_last_df=True)
            print('genereal analysis: (date, open and close are wrong!')
            print(k)
        else:
            print('total gain_ratio:')
            print(self.gain_ratio)
            print(str(self.gain_ratio*100) + '%')
            print('money:')
            print(self.money)





#when signal line crosses macd line a buy or sell is executed.
#It happens when diff passes 0 line.
class BasicSim(Simulation):
    #name

    def __init__(self, df, macd=None, signal=None, diff=None, path = 'datas',fromDisk = False,
                 num_of_sub=1, start=0, end=-1, sort_enabled = False, leverage=1):
        super().__init__(df,macd,signal,diff,path,fromDisk,num_of_sub, start, end, sort_enabled, leverage)
        self.name = 'Basic Simulation'

    def _determineBuySell(self):
        print('girdi2')
        buy = []
        sell = []

        tmp = 0
        i = 0
        for a in self.diff:
            if a == None:
                buy.append(False)
                sell.append(False)
            if tmp<0 and a>0:
                buy.append(True)
                sell.append(False)
                self._buy(i+1)
            elif tmp>0 and a<0:
                buy.append(False)
                sell.append(True)
                self._sell(i+1)
            else:
                buy.append(False)
                sell.append(False)
            tmp = a
            i += 1
        return buy, sell


#when signal line crosses and passes macd line in a length of a treshold value a buy or sell is executed.
#It happens when diff passes treshold value.
class BetterSim(Simulation):
    #name
    #treshold  its a rate

    def __init__(self, df, macd=None, signal=None, diff=None, path = 'datas',fromDisk = False,
                 num_of_sub=1, start=0, end=-1, sort_enabled = False, leverage=1):
        super().__init__(df,macd,signal,diff,path,fromDisk, num_of_sub, start, end, sort_enabled, leverage)
        self.name = 'Better Simulation'
        self.treshold = 0.00025    #negative values dont work
                                    #small values may work
                                    #0.000025 is the best
    def _determineBuySell(self):
        print('girdi')
        buy = []
        sell = []

        i = 0
        for a in self.diff:
            if a == None:
                buy.append(False)
                sell.append(False)
            trh = a / self.df['close'].iloc[i]
            if not self.bought and trh > self.treshold:
                buy.append(True)
                sell.append(False)
                self._buy(i + 1)
            elif self.bought and trh < self.treshold:
                buy.append(False)
                sell.append(True)
                self._sell(i + 1)
            else:
                buy.append(False)
                sell.append(False)
            i += 1
        return buy, sell


# TODO you need to normalize tresholds!
class ComplicatedSim(Simulation):
    # name
    # diff_treshold
    # trend_treshold

    def __init__(self, df, macd=None, signal=None, diff=None, path='datas', fromDisk=False,
                 num_of_sub=1, start=0, end=-1, sort_enabled = False, leverage=1):
        super().__init__(df, macd, signal, diff, path, fromDisk, num_of_sub, start, end, sort_enabled, leverage)
        self.name = 'Complicated Simulation'
        self.treshold = 300
        self.trend_treshold = 1000

    def _determineBuySell(self):
        print('girdi')
        buy = []
        sell = []

        i = 0
        for a in self.diff:
            trend = self.__findTrend(i)
            if a == None:
                buy.append(False)
                sell.append(False)

            if trend==1:
                if not self.bought and a > -self.treshold:
                    self._buy(i + 1)
                elif self.bought and a < -self.treshold:
                    self._sell(i + 1)
                else:
                    buy.append(False)
                    sell.append(False)
            elif trend==-1:
                if not self.bought and a > self.treshold:
                    self._buy(i + 1)
                elif self.bought and a < self.treshold:
                    self._sell(i + 1)
                else:
                    buy.append(False)
                    sell.append(False)
            else:
                if not self.bought and a > 0:
                    self._buy(i + 1)
                elif self.bought and a < 0:
                    self._sell(i + 1)
                else:
                    buy.append(False)
                    sell.append(False)
            i += 1
        return buy, sell


    def __findTrend(self, index):
        value = self.macd.iloc[index]
        if value == None:
            return 0

        if value > self.trend_treshold:
            return 1
        elif value < -self.trend_treshold:
            return -1
        else:
            return 0



