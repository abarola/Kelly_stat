

#####################################################################################################################
###################Estrazioni data corretta da yahoo finance



#from pandas_datareader import data as pdr
#import fix_yahoo_finance
#
#data1 = pdr.get_data_yahoo('ISP.MI', start='2016-04-23', end='2017-06-24')
#print data1

underlying="EPRE.MI"

import fix_yahoo_finance as yf
data = yf.download(underlying, start="1990-02-01", end="2017-08-03")



data= data.rename(columns={'Adj Close':'AdjClose'})
print
print data
data.to_csv(str(underlying) + ' datikelly.csv', index=True)










