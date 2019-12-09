#%% return rate
from matplotlib.gridspec import GridSpec

data = pandas.read_csv('event_data/summary.txt', header = None,sep='\t').iloc[:,:3]
data.columns=['event','date','npr']


data2 = data_all[data_all.parkrunner.str.find('Unknown')<0].parkrunner.value_counts()
data2 = data2[data2>1]

parkrunners=list(data2.index)
data3=[]
c=0

figure(figsize=(6,14))
no=[]
yes=[]
t=[]
for n,p in zip(data2,parkrunners):
    c+=1
    d=data_all[data_all.parkrunner==p]
    fi = d.event.iloc[0]
    if len(d)>1:
        iei = max(diff(d.event))
        eventplot(d.event,lineoffsets=-c,linewidths=6,linelengths=1,color='k')
        data3.append(list(hstack((fi,diff(d.event)))))
        t.append([p,max(diff(d.event))])
        yes.append(fi)
    else:
        no.append(fi)
        
yticks([])
ylim(-c-1,1)
xlabel('Event #')

#%%
yesratio=[]
noratio=[]
figure(figsize=(6,6))
subplot(211)
for i in arange(1,52):
    tft = sum(data_all[data_all.event==i].total_runs==1)
    yesratio.append(sum(array(yes)==i))
    noratio.append(sum(array(no)==i))
plot(arange(1,52),yesratio,'bo-',label='Yes')
plot(arange(1,52),noratio,'rs-',label='No')
ylabel('N parkrunner (first-timer)')
xlabel('first event #')
title('First event vs. whether they return at a later date')
legend()
subplot(212)
plot(arange(1,52),array(noratio)/array(yesratio),'kd')
ylabel('Ratio No:Yes')
xlabel('first event #')
plot([0,52],[1,1],'k:')
tight_layout()

#%%
for r in arange(0,50,10):
    dataflat=[]
    d2=array([x[0] for x in data3])
    dummy=[dataflat.extend(x[1:]) for x in data3 if (x[0]>r)&(x[0]<=(r+10))]
    y,x=histogram(array(dataflat),arange(1,max(dataflat)+2))
    plot(x[:-1],y/sum((d2>r)&(d2<=(r+10)))/len(dataflat),'.-',label=str(r)+'-'+str(r+10)+'; mean IEI: %.2g'%(mean(dataflat)))
xlabel('Inter-event interval')
ylabel('Normalized count')
legend()
