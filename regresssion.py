import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import predictor.utility as util
import datetime
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score


MAP_NUM = 100

#date1 = datetime.datetime.strptime("2015-01-30", "%d-%m-%y").strftime("%d.%m.%Y")

df = pd.read_csv('datas//bist30_d.csv', sep=',')

#print(df.head())

simdi = df['Simdi']
tarih = df['Tarih']

curr = util.str2float(simdi)
date = util.str2date(tarih)
time = util.date2timestamp(date)

for i in range(len(time)):
    time[i] = time[i]/1000000000
print('basladi')
x_mapped = util.map(time,MAP_NUM)
print('bitti')

print(x_mapped)

normalizer = preprocessing.StandardScaler().fit(x_mapped)
x = normalizer.transform(x_mapped)


one = np.ones((1,len(curr)),float)
x = np.insert(x, 0, one, axis=1)


x_train, x_test, y_train, y_test  = train_test_split(x, curr , train_size = 0.7, random_state =  90)


reg = linear_model.LinearRegression()
print('basla')
reg.fit(x_train, y_train)
print('bitir')

predict_train = reg.predict(x_train)
predict_test = reg.predict(x_test)
predict = reg.predict(x)

print(reg.coef_)


e_train = mean_squared_error(predict_train, y_train)

e_test = mean_squared_error(predict_test, y_test)

print(e_train)
print(e_test)


plt.plot(date, predict)
plt.plot(date, curr)

plt.show()