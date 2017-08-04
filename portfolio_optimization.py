import pandas as pd
import fix_yahoo_finance as yf
import numpy as np



pd.set_option('display.width', 1000)


#######################################################################################################################
#######################################################################################################################
####################################### Date inizio e fine

start = "2000-02-01"
end = "2017-08-03"


underlying = "IFEU" #(EPRE.MI)
data = yf.download(underlying, start=start, end=end)



################################## rinominare le colonne con il nome dello strumento
data = data.rename(columns={"Open": underlying + " Open", "High": underlying + " High", 'Low': underlying + ' Low',
                            'Close': underlying + ' Close', 'Adj Close': underlying + ' AdjClose',
                            'Volume': underlying + ' Volume'})
print list(data)


########################################################################################################################
########################################################################################################################
##########################################Secondo Underlying
underlying1 = "XWD.TO" #(SWDA.MI)
data1 = yf.download(underlying1, start=start, end=end)
data1 = data1.rename(columns={"Open": underlying1 + " Open", "High": underlying1 + " High", 'Low': underlying1 + ' Low',
                              'Close': underlying1 + ' Close', 'Adj Close': underlying1 + ' AdjClose',
                              'Volume': underlying1 + ' Volume'})


########################################################################################################################
########################################################################################################################
##########################################Terzo Underlying
underlying2 = "EAGG.PA" #(IEAG.MI)
data2 = yf.download(underlying2, start=start, end=end)
data2 = data2.rename(columns={"Open": underlying2 + " Open", "High": underlying2 + " High", 'Low': underlying2 + ' Low',
                              'Close': underlying2 + ' Close', 'Adj Close': underlying2 + ' AdjClose',
                              'Volume': underlying2 + ' Volume'})






print 'joined'
result = pd.merge(data, data1, left_index=True, right_index=True, how='outer') ##### mettere i due dataframe uno di fianco all'altro sulla base dellindice
result = pd.merge(result, data2, left_index=True, right_index=True, how='outer') ##### mettere i due dataframe uno di fianco all'altro sulla base dellindice
result =result.dropna()

print result
print list(result)



underlyings=[underlying, underlying1, underlying2]
for i in range(0, len(underlyings)):
    result.drop([underlyings[i] + " Open"], axis=1,inplace=True)
    result.drop([underlyings[i] + " High"], axis=1,inplace=True)
    result.drop([underlyings[i] + " Low"], axis=1,inplace=True)
    result.drop([underlyings[i] + " Volume"], axis=1,inplace=True)
    result.drop([underlyings[i] + " Close"], axis=1,inplace=True)
    result[underlyings[i] +' log_ret'] = np.log(result[underlyings[i] + ' AdjClose']) - np.log(result[underlyings[i] + ' AdjClose'].shift(1)) #### calcola i ritorni logaritmici
    result.drop([underlyings[i] + " AdjClose"], axis=1,inplace=True)



print
print 'correlation'
print result.corr()
print
print 'covarriance'
print result.cov()
print
print 'mean'
print result.mean()





mean= np.array(result.mean())
w=np.array((0.33,0.33,0.33))
cov= np.matrix(result.cov())



Var = np.transpose(w) * np.matrix(result.cov())
Var = np.dot(Var, w)


yearlystd= np.sqrt(Var) * np.sqrt(252)
yearlymean=np.dot(mean, w) *252
print yearlystd
print yearlymean

lowerband = yearlymean -3*yearlystd
upperband = yearlymean +3*yearlystd

print
print 'lowerband'
print lowerband
print
print 'upperband'
print upperband

