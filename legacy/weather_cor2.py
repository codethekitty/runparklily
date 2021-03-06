#!/usr/bin/env python3
import pandas
from pylab import *

#%% get date
from datetime import datetime

D=import_data.import_result()

data = pandas.read_csv('../other_data/summary.txt', header = None,sep='\t').iloc[:,:3]
data.columns=['event','date','npr']
data.date = [datetime.strptime(x,'%d/%m/%Y') for x in list(data.date)]


#% get weather data
weather = pandas.read_csv('../other_data/1956002.csv', header=0,sep=',')
weather.DATE = [datetime.strptime(x,'%Y-%m-%d') for x in list(weather.DATE)]
weather = weather.loc[:,['DATE','AWND','PRCP','SNOW','SNWD','TMAX','TMIN','TOBS']]
#%
m=[]
ft=[]
for n,d in data.iterrows():
    w = weather[weather.DATE==d.date].iloc[:,1:].mean()
    m.append(w.values)
    nfirsttimer=sum(D[D.event==d.event].note.str.find('First T')==0)
    ntotal=sum(D.event==d.event)
    ft.append([nfirsttimer,ntotal])
    
m=pandas.DataFrame.from_records(m,columns=list(w.index))
ft=pandas.DataFrame.from_records(ft,columns=['n_1','n_total'])
df = pandas.concat([data,m,ft],axis=1)

df.iloc[0,3:-2]=array([2.2,0,0,0,nan,nan,-2.2])








#%%
colors=rcParams['axes.prop_cycle'].by_key()['color']
from matplotlib.gridspec import GridSpec
from scipy.stats import linregress

figure(figsize=(8,4))
gs=GridSpec(2,1,height_ratios=(2,1))

subplot(gs[0])
plot(df.date,df.npr,'o-',ms=4,color=colors[0],label='Total')
plot(df.date,df.n_total-df.n_1,'d-',ms=4,color=colors[1],label='Returners')
plot(df.date,df.n_1,'s-',ms=4,color=colors[2],label='First timers')
ylabel('Attendance')
legend(loc=2)


v='TOBS'
l='Temperature (C/F)'
subplot(gs[1])
plot(df.date,df[v],'o-',ms=4,color=colors[3])
ylabel(l)

tc=arange(-10,30,10)
yticks(tc,[str(x)+' / '+str(int(x*9/5+32)) for x in tc])

xlabel('Year-Month')

tight_layout()
savefig('../../temp11.jpg',dpi=150,bbox_inches='tight')

#%%
figure(figsize=(6,2.5))
from datetime import timedelta
import import_data


name = 'Joshua S'
D=D[D.parkrunner.str.find(name)>=0].loc[:,['time','event']]
D2=pandas.DataFrame(columns=list(df))
for i in D.event:
    D2=pandas.concat((D2,df[df.event==i]))
D=pandas.concat([D.reset_index(),D2.reset_index()],axis=1)
D.time=[timedelta(minutes=int(x[-5:-3]),seconds=int(x[-2:])) for x in list(D.time)]
D=D.iloc[:,[1,2,5,6,7,8,9,10,11,12,13]]
Dbackup=D
i=where(D.time>timedelta(minutes=40))[0][0]
D=D[D.time<timedelta(minutes=40)]
plot(D.date,[x.total_seconds()/60 for x in D.time],'o-',color='k')
plot(Dbackup.iloc[i].date,24.8,'x',color='k',ms=7)
#X,Y=(D.time.dt.seconds/60,D.TOBS)
#m,b,r,p,s = linregress(X,Y)
#xl=linspace(min(X),max(X),2)
#yl=xl*m+b
#print('r=%.2f, p=%.4f'%(r,p))
title('Josh\'s finish time')
ylabel('Time (min)')

ylim(18,25)
xlabel('Year-Month')
tight_layout()
#savefig('../temp1.jpg',dpi=150,bbox_inches='tight')



#%%
from scipy.stats import linregress


figure(figsize=(12,4))
subplot(223)
y=df[v]
x=array([int(x) for x in df.date.values])
plot(x,y,'o',color=colors[3])
f = poly1d(polyfit(x,y,5))
plot(x,f(x),'k')
xticks([])
title('Trend Fitting for Temperature')

subplot(224)
plot(x,y-f(x),'o-',color=colors[3])
#xsel=x[::9]
#ll=[str(x)[:7] for x in pandas.to_datetime(xsel)]
#xticks(xsel,ll)
xticks([])
title('De-trended Temperature')
dey1=y-f(x)

subplot(221)
y=df.npr
x=array([int(x) for x in df.date.values])
plot(x,y,'o',color=colors[0])
f = poly1d(polyfit(x,y,3))
plot(x,f(x),'k')
xticks([])
title('Trend Fitting for Attendance')

subplot(222)
plot(x,y-f(x),'o-',color=colors[0])
xticks([])
title('De-trended Attendance')
dey2=y-f(x)

savefig('../../temp2.jpg',dpi=150,bbox_inches='tight')

#figure()
#plot(dey1,dey2,'ks')
#m,b,r,p,s = linregress(dey1,dey2)
#xl=linspace(min(dey1),max(dey1),2)
#yl=xl*m+b
#plot(xl,yl,'k-')
#title('r=%.2f, p=%.4f'%(r,p))