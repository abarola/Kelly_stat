import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 100)

pd.set_option('display.width', 1000)



############# dati dinamici che e possibile modificare
underlying='EPRE.MI'
window=90 #### lunghezza della media mobile
conservatism = 0.75 #### percentuale di kelly fraction data incertezza nel calcolo dei dati
leva=1
initial_wealth=1000
resamplingday=60 ##### periodo di ribilanciamento (1=1 gg)
tradingcost=12.5 #### ammontare assoluto di trading cost



#data = pd.read_excel('ispdatistorici.xlsx')
data = pd.read_csv(str(underlying)+' datikelly.csv')
data['Date'] = data['Date'].astype('datetime64[ns]')



############################## gestione dei dati
data['log_ret'] = np.log(data.AdjClose) - np.log(data.AdjClose.shift(1)) #### calcola i ritorni logaritmici
data['mean']=pd.rolling_mean(data.log_ret.shift(),window) ##### importante shift() la media mobile non deve considerare il ritorno del giorno ma solo giorni precedenti
data['std']=pd.rolling_std(data.log_ret.shift(),window) ##### importante shift() la media mobile non deve considerare il ritorno del giorno ma solo giorni precedenti
data['var']= data['std']**2
data['kelly'] = data['mean']/data['var']
data['kelly'] = data['kelly'].apply(lambda x: x*conservatism) #### applica la percentuale di conservatism a kelly
data.loc[data['kelly']<0,'kelly'] =0 ###### sostituisce numeri negativi in colonna con zero ( non permette shorselling
data.loc[data['kelly']>leva,'kelly'] =leva ###### sostituisce numeri superiori a leva in colonna con leva ( serve a gestire leverage)
data1=data.copy()
data1= data1.dropna() #### elimina rows con NaN
data1['perc_ret']=data1['AdjClose'] /data1['AdjClose'].shift(1) #### calcola i ritorni normali
data1['perc_ret_kelly']=(data1['AdjClose'] /data1['AdjClose'].shift(1)-1) * data1['kelly'].shift(1) + 1 #### calcola i ritorni normali
data1['wealth_growth'] = (data1.perc_ret_kelly).cumprod() * initial_wealth
data1= data1.dropna() #### elimina rows con NaN
########################################################################################################################
########################################################################################################################
####provare a fare resampling
data2=data1.copy()
data2= data2.iloc[::resamplingday, :]
data2['perc_ret']=data2['AdjClose'] /data2['AdjClose'].shift(1) #### calcola i ritorni normali
data2['perc_ret_kelly']=(data2['AdjClose'] /data2['AdjClose'].shift(1)-1) * data2['kelly'].shift(1) + 1 #### calcola i ritorni normali
data2['wealth_growth'] = (data2.perc_ret_kelly).cumprod() * initial_wealth
data2.to_csv('resamplekelly.csv', index=True)
data2 = data2.dropna() #### elimina rows con NaN
print
print 'data2'
print data2
########################################################################################################################
########################################################################################################################
####inserimento costi di transazione
data3=data2.copy()
##data3['trading_cost']= 10
data3['trading_cost']=np.where(data3.kelly.eq(data3.kelly.shift()),0,10) ### si inseriscono trading cost solo dove frazione investita cambia
data3['trading_cost']= data3.trading_cost.cumsum()
data3['netwealth']= data3['wealth_growth']- data3['trading_cost']
print data3
########################################################################################################################
########################################################################################################################
##################### calcolo statistiche
endwealth= data3['netwealth'][data3.index[-1]]
totret= endwealth/initial_wealth




import matplotlib.pyplot as plt

plt.figure(1)
plt.subplot(211)
plt.plot(data1['Date'], data1['AdjClose'])
plt.subplot(212)
axes = plt.gca()
axes.set_ylim([-1,1.5])
plt.plot(data1['Date'], data1['kelly'])


fig, ax1 = plt.subplots()
ax1.plot(data1['Date'], data1['AdjClose'], 'b-')
ax2 = ax1.twinx()
ax2.plot(data1['Date'], data1['kelly'], 'r-')
ax2.axes.set_ylim([-0.1,1.1])
fig.tight_layout()


fig, ax1 = plt.subplots()
ax1.plot(data1['Date'], data1['AdjClose'], 'b-')
ax2 = ax1.twinx()
ax2.plot(data1['Date'], data1['wealth_growth'], 'r-')
fig.tight_layout()


fig, ax1 = plt.subplots()
ax1.plot(data3['Date'], data3['AdjClose'], 'b-')
ax1.set_title('ribilanciamento ogni ' + str(resamplingday) + ' giorni con costi di transazione')
ax2 = ax1.twinx()
ax2.plot(data3['Date'], data3['netwealth'], 'r-')
fig.tight_layout()


plt.show()