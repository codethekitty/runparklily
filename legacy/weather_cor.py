import pandas
from pylab import *

#%% get date
from datetime import datetime

data = pandas.read_csv('../other_data/summary.txt', header = None,sep='\t').iloc[:,:3]
data.columns=['event','date','npr']
data.date = [datetime.strptime(x,'%d/%m/%Y') for x in list(data.date)]


#% get weather data
weather = pandas.read_csv('../other_data/1956002.csv', header=0,sep=',')
weather.DATE = [datetime.strptime(x,'%Y-%m-%d') for x in list(weather.DATE)]
weather = weather.loc[:,['DATE','AWND','PRCP','SNOW','SNWD','TMAX','TMIN','TOBS']]
#%
m=[]
for n,d in data.iterrows():
    w = weather[weather.DATE==d.date].iloc[:,1:].mean()
    m.append(w.values)
m=pandas.DataFrame.from_records(m,columns=list(w.index))
df = pandas.concat([data,m],axis=1)

df.iloc[0,3:]=array([2.2,0,0,0,nan,nan,-2.2])

#%%
colors=rcParams['axes.prop_cycle'].by_key()['color']
from matplotlib.gridspec import GridSpec
from scipy.stats import linregress

figure(figsize=(8,10))
gs=GridSpec(5,2,width_ratios=(3,1))
var = zip(['TOBS','PRCP','SNOW','AWND'],['Temperature (C/F)','Precipitation (mm)','Snow fall (mm)','Wind speed (m/s)'])
subplot(gs[0,0])
plot(df.date,df.npr,'o-',ms=4,color=colors[0])
ylabel('Attendance')
#subplot(gs[0,1])
#text(0,0,'Effect of weather on Lillie attendance',fontsize=12,ha='center')
#grid('on')

ss=0
for v,l in var:
    ss+=1
    
    subplot(gs[ss,0])
    plot(df.date,df[v],'o-',ms=4,color=colors[ss])
    ylabel(l)
    
    subplot(gs[ss,1])
    X,Y=(df.npr.values,df[v].values)
    X=X[~isnan(Y)]
    Y=Y[~isnan(Y)]
    plot(X,Y,'ko',ms=4)
    m,b,r,p,s = linregress(X,Y)
    xl=linspace(min(X),max(X),2)
    yl=xl*m+b
    plot(xl,yl,'k:')
    title('r=%.2f, p=%.4f'%(r,p))
#    if ss==1:
#        tc=arange(-10,30,10)
#        yticks(tc,[str(x)+' / '+str(int(x*9/5+32)) for x in tc])
tight_layout()


#%%
from datetime import timedelta
colors=rcParams['axes.prop_cycle'].by_key()['color']

names = ['Adam H','Emma K','Stephanie E','Amanda P','Calvin W','Kelly S']
ss=0
figure(figsize=(8,8))
for name,col in zip(names,colors[:len(names)]):
    ss+=1
    subplot(3,2,ss)
    D=data_all[data_all.parkrunner.str.find(name)>=0].loc[:,['time','event']]
    D2=pandas.DataFrame(columns=list(df))
    for i in D.event:
        D2=pandas.concat((D2,df[df.event==i]))
    D=pandas.concat([D.reset_index(),D2.reset_index()],axis=1)
    D.time=[timedelta(minutes=int(x[-5:-3]),seconds=int(x[-2:])) for x in list(D.time)]
    D=D[(D.time>timedelta(minutes=15))&(D.time<timedelta(minutes=40))]
    plot(D.time.dt.seconds/60,D.TOBS,'o',label=name,color=col)
    X,Y=(D.time.dt.seconds/60,D.TOBS)
    m,b,r,p,s = linregress(X,Y)
    if p<0.05:
        xl=linspace(min(X),max(X),2)
        yl=xl*m+b
        plot(xl,yl,'-',color=col)
        text(xl[-1],yl[-1],'r=%.2g'%(r),color=col,fontsize=12)   
    ylabel('Temperature (C)')
    xlabel('Finish time (min)')
    title(name,color=col)
tight_layout()


#savefig('temp.jpg',dpi=150,bbox_inches='tight')




