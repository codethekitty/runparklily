#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pylab import *
import pandas, glob
from scipy.stats import zscore
from datetime import datetime

#%%
ff = glob.glob('attendance_data/*')
h = ['event','date','npr','nv']
predictionresult=[]
for i in ff:
    figure()
    df = pandas.read_csv(i,'\t',header=None)
    df = df.iloc[:,:4]
    df.columns=h
    x=df.event
    y=df.npr
    predict=[]
    for d in arange(3,18):
        f = poly1d(polyfit(x,y,d))
        plot(x,y,'o-')
        plot(x,f(x),'-')
        if (f(max(x)+1)<(max(y)*2)) & (f(max(x)+1)>0) & (f(max(x)+1)>y.values[0]/2):
            plot(max(x)+1,f(max(x)+1),'s')
            predict.append([max(x)+1,f(max(x)+1)])
#    plot(x,y,'o-')
    pattn = array(predict)[:,1]
    mpattn=mean(pattn)
    errorbar(max(x)+2,mpattn,std(pattn),marker='s')
    title('%s: %d'%(i[16:-4],mpattn))
#    savefig('../../fig/{nn}.png'.format(nn=i[16:-4]),dpi=65,bbox_inches='tight')

    d=[datetime.strptime(x,'%d/%m/%Y') for x in df.date.values]
    dd=[abs(x.days) for x in diff(d)]
    w=where(array(dd)==2)[0]
    if len(w)>0:
        for i2 in w:
           thxgiving=df.date.iloc[i2+1]
           actual=df.npr.iloc[i2+1]
           expected=f(x)[x==df.event.iloc[i2+1]][0]      
           predictionresult.append([i[16:-4],mpattn,actual,expected])
    else:
        predictionresult.append([i[16:-4],mpattn,nan,nan])

p = pandas.DataFrame.from_records(predictionresult,columns=['parkrun','next_day_prediction','actual_thxgiving_att','expected_thxgiving_att'])

#%%

p['delta_thxgiving']=p.actual_thxgiving_att-p.expected_thxgiving_att
p.round().to_csv('../../thxgiving.csv')
p['thxgiving_prediction']=p.next_day_prediction+p.delta_thxgiving
pmean = p.groupby('parkrun').mean().round()
pmean.to_csv('../../thxgiving_prediction.csv')
