from pylab import *
import import_data,pandas
df = import_data.import_result()
df2 = import_data.import_volunteer()
#%% adam vs steph
        
#op = data_all[data_all.note.str.find('First Timer!')==0].groupby('event').count().pos

aa = data_all[data_all.parkrunner.str.find('Adam HOCKLEY')>=0]
y = [float(x[:-2]) for x in aa.age_grade.values]
x = aa.event.values
plot(x,y,'o-',label='Adam')

aa = data_all[data_all.parkrunner.str.find('Stephanie EVANS')>=0]
y = [float(x[:-2]) for x in aa.age_grade.values]
x = aa.event.values
plot(x,y,'o-',label='Steph')

xlim(0,43)
ylim(0,100)
xlabel('Event #')
ylabel('Age Grade %')
legend()

savefig('age_grade.jpg',dpi=150,bbox_inches='tight')

#%% pacer analysis
from datetime import datetime

data = data_all[data_all['event']==43]
pacers=['Joshua S','Adam S','Calvin W','Tim K',\
        'Christopher F','Alison R','Savio P','Kranthi B']
target=[20,22,24,26,28,30,34,36]
targetts=array(target)*60
actual=[]
for n in pacers:
    actual.append(data[data.parkrunner.str.find(n)>=0].time.values[0])
actualts=array([int(x[:2])*60+int(x[-2:]) for x in actual])

figure(figsize=(10,2))

delta=[]
for i,n in enumerate(pacers):
    plot([targetts[i]]*2,[0,2],'k-')
    plot(actualts[i],1,'bo',ms=8)
    d=actualts[i]-targetts[i]
    plot([actualts[i],actualts[i]],[1,2.05],'r:')
    text(actualts[i],2.05,str(d)+'\"',ha='center',color='r')
#    text(actualts[i],0.4,n,color='b',rotation=-45)
    delta.append(d)
    
ylim(0,2)
xticks(targetts,[str(x)+'\'' for x in target])
yticks([])

savefig('pacer2.jpg',dpi=150,bbox_inches='tight')


#%% previous event time analysis
figure(figsize=(10,2))


data = data_all[(data_all['event']<43)&(data_all['event']>39)]
data = data[data.time.str.len()==5].time.values
timedist=array([int(x[:2])*60+int(x[-2:]) for x in data])
xran=arange(18,45,2)*60
hist(timedist,xran,color='y',edgecolor='k')
xticks(xran,[str(x)[:2]+'\'' for x in xran/60])

ylabel('# parkrunners')
xlabel('finish time')
title('Distribution of finish time in previous events (lillie #40~#42)')

savefig('pacer1.jpg',dpi=150,bbox_inches='tight')

#%% number of PBs
nfinisher=[]
for i in range(2,45):
    data = data_all[data_all['event']==i]
    data2 = data[data.note.str.find('First Timer')>=0]
    bar(i,len(data2),1,facecolor='y',edgecolor='k')
    nfinisher.append([i,len(data2)])
#    bar(i,len(data2)/len(data)*-100,1,facecolor='m',edgecolor='k')
#xticks(range(30,44))
#yl=hstack((arange(-30,0,10),arange(0,25,5)))
#yticks(yl,[str(x) for x in abs(yl)])
xlabel('event #')
#ylabel('% PB\'s ----------- # of PB\'s')
#text(43,17,'Pacer day',ha='center')

#savefig('pacer13jpg',dpi=150,bbox_inches='tight')

#%% first names
fnames=unique(data_all.parkrunner)
notsurname=[]
for r in fnames:
    names=r.split(' ')
    surname=[]
    for f in names:
        if f.isupper():
            surname.append(f)
    firstname=array(names)[~isin(names,surname)]
    notsurname.append(' '.join(firstname))

N=[]
for n in unique(notsurname):
    ct = notsurname.count(n)
    N.append({'name':n,'count':ct})

#six = argsort(array(list(N.values())))
#namefreq = array(list(N.keys()))[six]            

L=pandas.DataFrame(N)

#%%
u=unique(data_all.parkrunner)
u=u[~isin(u,'Unknown')]
df=[]
for n in u:
    d=data_all[data_all.parkrunner==n].iloc[-1,:].age_cat[2:4]
    g=data_all[data_all.parkrunner==n].iloc[-1,:].age_cat[1]
    h=data_all[data_all.parkrunner==n].iloc[-1,:].age_cat
    if len(h)<7:
        h2=int(d)
    else:
        h2=int(h[5:])
    df.append({'gender':g,'age1':int(d),'age2':h2})
df=pandas.DataFrame(df)
#%% age cat

figure(figsize=(10,3))
for i in ['M','W']:
    h=histogram(df[df.gender==i].age1,unique(df.age1))[0]
    plot(range(len(h-1)),h,'-o')
label=[]
for i,j in zip(unique(df.age1),unique(df.age2)):
    if i==j:
        L=str(i)
    else:
        L=str(i)+'-'+str(j)
    label.append(L)
xticks(range(len(h-1)),label,rotation=45)
xlabel('Age Category')
ylabel('# Parkrunner')
legend(('Male','Female'))

savefig('age_distribution.jpg',dpi=300,bbox_inches='tight')

#%% 
data=data_all.groupby('parkrunner').count().pos.reset_index()
data=data[data.parkrunner!='Unknown']
figure(figsize=(10,3))
ax=gca()
x=arange(0.5,max(data.pos)+1.5,1)
y=histogram(data.pos,x)[0]
ax.bar(x[:-1]+0.5,y,1,facecolor='y',edgecolor='k')
xlim(0,45)
ylim(0,100)
ax.annotate('283',xy=(0.7,95),xytext=(3,90),arrowprops=dict(facecolor='black',arrowstyle='->'))
ax.annotate('Scott',xy=(44,3),xytext=(43,20),arrowprops=dict(facecolor='black',arrowstyle='->'))

xlabel('# of events attended')
ylabel('# parkrunners')

savefig('repeaters.jpg',dpi=300,bbox_inches='tight')



#%% n of pbs table

allpb=[]
for event in range(48-12,48):
    df=data_all[data_all.event==event]
    pb = df[df.note.str.find('New PB!')==0]
    allpb.extend(pb.parkrunner.values)
tbl = pandas.Series(data=allpb).value_counts()

#%% 
data = data_all[data_all.parkrunner.str.find('David BERTCHER')==0]
ag = [float(x[:5]) for x in data.age_grade]
figure(figsize=(10,3))
plot(data.event,ag,'ro-')
text(34,60,'Jaime D',color='b')

data = data_all[data_all.parkrunner.str.find('Jaime DUDASH')==0]
ag = [float(x[:5]) for x in data.age_grade]
plot(data.event,ag,'bo-')
text(39,50,'David B',color='r')

xlabel('Event #')
ylabel('Age Grade %')
xticks(arange(32,47))
title('The impressive feats')

savefig('PB.jpg',dpi=300,bbox_inches='tight')

#%%

decitime=[]
for i,n in df.iterrows():
    tstr=n.time
    tlist=tstr.split(':')
    if len(tlist)==3:
        tt = float(tlist[1])+float(tlist[2])/60+60
    else:
        tt = float(tlist[0])+float(tlist[1])/60
    decitime.append(tt)
df['decitime']=decitime

allpr = df.parkrunner.value_counts()
allpr = list(allpr[allpr>9].index)
allcv=[]
for pr in allpr:
    tt = df[df.parkrunner.str.find(pr)==0].decitime
    cv = std(tt)/mean(tt)
    allcv.append(cv)
data=pandas.DataFrame({'nom':array(allpr),'cv':array(allcv)})
print(data.sort_values(by='cv'))




