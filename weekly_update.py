import matplotlib.patches as patches
from numpy.matlib import repmat
from matplotlib import gridspec

#%% first name teams

D = df[df.parkrun=='Lillie parkrun, Ann Arbor']
firstnames = [x.split(' ') for x in D.parkrunner]
N=[]
for i in firstnames:
    if i[0].find('.')>=0:
        n=i[1]
    else:
        n=i[0]
    N.append(n)
stat=[]
for u in unique(N):
    ix=isin(N,u)
    cc=len(unique(D[ix].parkrunner))
    if cc>1:
        Dsub={}
        for n in unique(D[ix].parkrunner):
            D2=D[ix][D[ix].parkrunner==n]            
            tall=[]
            for t in D2.time:
                if len(t)<6:
                    tall.append(int(t[:t.find(':')])+int(t[t.find(':')+1:])/60)
                else:
                    tlist=[int(x) for x in t.split(':')]
                    tall.append(tlist[0]*60+tlist[1]+tlist[2]/60)
            Dsub[n]=(sum(D[ix].parkrunner==n),min(tall))
        stat.append({'fname':u,'count':cc,'total_runs':sum(ix),'detail':Dsub})
stat=pandas.DataFrame.from_dict(stat)
stat=stat.sort_values(by='total_runs',ascending=False).reset_index().drop(columns='index')
stat=stat[(stat.total_runs/stat['count'])>1].reset_index().drop(columns='index')


def get_color(t):
    tnorm = (t-18)/(40-18)
    c=matplotlib.cm.get_cmap('viridis')(tnorm)
    return c

fig, ax = subplots(figsize=(16,28))
xt=[]
for i,j in stat.iterrows():
    v=0
    for k,(v1,v2) in j.detail.items():
        rect = patches.Rectangle((v,len(stat)-i-0.5),v1,1,linewidth=1,edgecolor='w',facecolor=get_color(v2))
        if v1>2:
            ln=k.split(' ')[-1]
            if v2<30:
                c2='w'
            else:
                c2='k'
            text(mean([v,v+v1]),len(stat)-i,ln,ha='center',va='center',fontsize=11-2*len(ln)/v1,color=c2)
        v+=v1
        ax.add_patch(rect)
    xt.append(j.fname+': '+str(j['count']))
ylim(0,len(stat)+1)
xlim(0,stat.total_runs[0]+1)
yticks(arange(len(xt))+1,xt[::-1],ha='right')
ax.set_xlabel('Total Runs',fontsize=12)
ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top') 
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)

cmap=matplotlib.cm.get_cmap('viridis')
colors=cmap(arange(40-18))
ax2 = fig.add_axes([0.80, 0.55, 0.1, 0.2])
ax2.imshow(repmat(arange(18,40,0.1),10,1).T)
ax2.set_xticks([])
ax2.set_yticks(arange(0,240,20))
tick=[str(int(x)) for x in linspace(18,40,12)]
tick[0]='<18'
tick[-1]='40+'
ax2.set_yticklabels(tick)
ax2.set_ylabel('PB (min)')

fn = datetime.datetime.now().strftime('%Y.%m.%d')
tt='(updated %s)'%(fn)
title(tt,fontweight='normal',fontsize=10,loc='left')

savefig('shared/figures/firstname_team.png',dpi=300,bbox_inches='tight')
print('updated run league tables (first name)')

#%% last name teams

firstnames = [x.split(' ') for x in D.parkrunner]
N=[]
for i in firstnames:
    n=i[-1]
    N.append(n)
stat=[]
for u in unique(N):
    ix=isin(N,u)
    cc=len(unique(D[ix].parkrunner))
    if cc>1:
        Dsub={}
        for n in unique(D[ix].parkrunner):
            D2=D[ix][D[ix].parkrunner==n]            
            tall=[]
            for t in D2.time:
                if len(t)<6:
                    tall.append(int(t[:t.find(':')])+int(t[t.find(':')+1:])/60)
                else:
                    tlist=[int(x) for x in t.split(':')]
                    tall.append(tlist[0]*60+tlist[1]+tlist[2]/60)
            Dsub[n]=(sum(D[ix].parkrunner==n),min(tall))
        stat.append({'fname':u,'count':cc,'total_runs':sum(ix),'detail':Dsub})
stat=pandas.DataFrame.from_dict(stat)
stat=stat.sort_values(by='total_runs',ascending=False).reset_index().drop(columns='index')
stat=stat[(stat.total_runs/stat['count'])>1].reset_index().drop(columns='index')

fig, ax = subplots(figsize=(16,28))
xt=[]
for i,j in stat.iterrows():
    v=0
    for k,(v1,v2) in j.detail.items():
        rect = patches.Rectangle((v,len(stat)-i-0.5),v1,1,linewidth=1,edgecolor='w',facecolor=get_color(v2))
        if v1>2:
            nn=k.split(' ')
            if nn[0].find('.')>=0:
                ln=nn[1]
            else:
                ln=nn[0]
            if v2<30:
                c2='w'
            else:
                c2='k'
            text(mean([v,v+v1]),len(stat)-i,ln,ha='center',va='center',fontsize=11-2*len(ln)/v1,color=c2)
        v+=v1
        ax.add_patch(rect)
    xt.append(j.fname+': '+str(j['count']))
ylim(0,len(stat)+1)
xlim(0,stat.total_runs[0]+1)
yticks(arange(len(xt))+1,xt[::-1],ha='right')
ax.set_xlabel('Total Runs',fontsize=12)
ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top') 
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)

cmap=matplotlib.cm.get_cmap('viridis')
colors=cmap(arange(40-18))
ax2 = fig.add_axes([0.80, 0.55, 0.1, 0.2])
ax2.imshow(repmat(arange(18,40,0.1),10,1).T)
ax2.set_xticks([])
ax2.set_yticks(arange(0,240,20))
tick=[str(int(x)) for x in linspace(18,40,12)]
tick[0]='<18'
tick[-1]='40+'
ax2.set_yticklabels(tick)
ax2.set_ylabel('PB (min)')

fn = datetime.datetime.now().strftime('%Y.%m.%d')
tt='(updated %s)'%(fn)
title(tt,fontweight='normal',fontsize=10,loc='left')

savefig('shared/figures/lastname_team.png',dpi=300,bbox_inches='tight')
print('updated run league tables (last name)')


#%% volunteer individual league table

current_count=df2.groupby('parkrun').max().event
dfv=df2.volunteer.value_counts()
dfv=dfv[dfv>24]
table=[]
for pr,n in dfv.items():
    homepr = df2[df2.volunteer==pr].parkrun.value_counts().idxmax()
    rr=sum((df.parkrunner==pr)) #(df.parkrun==homepr)
    if rr==0:
        p=inf
    else:
        p=n/rr
    pstr='%d/%d'%(n,rr)
    table.append({'parkrunner':pr,'n_volunteer':n,'home_parkrun':homepr, \
                  'vol/run':pstr,'ratio':p})

table=pandas.DataFrame.from_dict(table).sort_values(by=['ratio','n_volunteer'],ascending=False)
table=table.iloc[:200,:]
table['rank']=arange(1,201)
table=table.drop(['ratio','n_volunteer'],axis=1)

table.to_csv('shared/figures/top200_volunteers.csv',index=False)
print('updated volunteer')

#%% passionistas

passionistas=[]
for pr in df.parkrun.unique():
    thisparkrun = df[df.parkrun==pr]
    otherparkrun = df[df.parkrun!=pr]
    parkrunner_list = thisparkrun.parkrunner.value_counts()
    if (pr.find('Bear Creek')>-1)|(pr.find('Third')>-1):
        crit=0
    else:
        crit=5
    parkrunner_list = parkrunner_list[parkrunner_list>crit]
    count=0
    parkrunmax=thisparkrun.event.max()
    for p,i in parkrunner_list.items():
        check = sum(otherparkrun.parkrunner==p)
        if not bool(check):
            tprs = thisparkrun[thisparkrun.parkrunner==p].nprs.values
            tprs = max([int(x[:x.find('parkrun')-1]) for x in tprs])
            iprs = sum(thisparkrun.parkrunner==p)
            if iprs==tprs:
                passionistas.append({'parkrun':pr,'parkrunner':p,'count':i,'percentage':i/parkrunmax*100})
                print(pr,p,i)
                if (i/parkrunmax*100)<30:
                    break

#%%
P=pandas.DataFrame.from_dict(passionistas)
P2=P.sort_values('percentage',ascending=False)
P2['rank']=arange(1,len(P2)+1)
P2=P2.iloc[:50,:]
P2.percentage=around(P2.percentage,1)
P2.to_csv('shared/figures/top50_passionistas.csv',index=False)

# for pr in P.parkrun.unique():
#     top3 = P[P.parkrun==pr].sort_values(by='count',ascending=False).iloc[:3,:]
#     maxevent = max(df[df.parkrun==pr].event)
#     top3['parkrun_max']=maxevent
#     if pr==P.parkrun.unique()[0]:
#         P2=top3
#     else:
#         P2=pandas.concat((P2,top3))
        
# cc=rcParams['axes.prop_cycle'].by_key()['color']
# cc*=5
# mm = dict(zip(df.parkrun.unique(),arange(len(df.parkrun.unique()))))
# P3=P2.iloc[::-1,:].reset_index().iloc[:,1:]
# colorcode = P3.parkrun.map(mm)
# P3['color']=colorcode
# figure(figsize=(10,30))
# for i,j in P3.iterrows():
#     barh(i,j['count'],facecolor=cc[j['color']])
#     plot((j['count'],j['parkrun_max']),[i,i],color=cc[j['color']])
# #    plot(j['parkrun_max'],i,'o',color=cc[j['color']])
#     text(j['parkrun_max']+5,i,j['runner'],ha='left',va='center',color=cc[j['color']])
#     text(j['count']/2,i,'%d'%(j['count']),ha='center',va='center',color='w',fontsize=9)
# xt=arange(1,len(P3),3)
# xtl=[x[:x.find('parkrun')-1] for x in df.parkrun.unique()[::-1]]
# yticks(xt,xtl)
# ylim(-1,len(P3))
# title('Top 3 Passionistas of each parkrun')
# fn = datetime.datetime.now().strftime('%Y.%m.%d')
# tt='(updated %s)'%(fn)
# title(tt,fontweight='normal',fontsize=10,loc='right')
# xlabel('# Events')
       
# savefig('shared/figures/passionistas.png',dpi=300,bbox_inches='tight')

print('updated passionistas')

#%%

parkrunlist = list(df.parkrun.unique())
result=[]
for p in parkrunlist:
    leaders = df[df.parkrun==p].parkrunner.value_counts()
    leaders=leaders[leaders>max(leaders)/10]
    leaders=leaders.index
    print(len(leaders),df[df.parkrun==p].event.max())
    most_conseq_parkrun=[]
    for leader in leaders:
        a=sort(df[(df.parkrun==p) & (df.parkrunner==leader)].event.values)
        if all(diff(a)>0):
            count=1
            last_value=a[0]
            countS=[]
            for i in a[1:]:
                if i==last_value+1:
                    count+=1
                else:
                    countS.append(count)
                    count=1
                last_value=i
            if len(countS)>0:
                most_conseq=max(countS)
            else:
                most_conseq=len(a)
            conseq_loc=[]
            for i in range(len(a)):
                if len(a[i:i+most_conseq])==most_conseq:
                    if std(diff(a[i:i+most_conseq]))==0:
                        conseq_loc=a[i:i+most_conseq]
            cur=df[df.parkrun==p].event.max()
            # most_conseq_parkrun.append(most_conseq)
        # if most_conseq>=max(most_conseq_parkrun):
            if most_conseq>2:
                result.append({'parkrun':p,'leader':leader,'most_conseq':most_conseq,'events':conseq_loc,'current':cur})
                print(p,leader,most_conseq)
                    

conseq=pandas.DataFrame.from_dict(result)

#% top 50
dfsorted = conseq.sort_values('most_conseq',ascending=False)
export_table=[]
for i in range(50):
    rr = min(dfsorted.iloc[i,:].events),max(dfsorted.iloc[i,:].events)
    if rr[1]==dfsorted.iloc[i,:].current:
        rr2='ongoing'
    else:
        rr2=rr[1]
    rn = dfsorted.iloc[i,:].most_conseq
    rp = dfsorted.iloc[i,:].parkrun
    export_table.append({'rank':i+1,'streak':rn,'parkrunner':dfsorted.iloc[i,:].leader, \
                         'parkrun':dfsorted.iloc[i,:].parkrun, \
                         'streak_start':rr[0],'streak_end':rr2})
export_table=pandas.DataFrame.from_dict(export_table)
export_table.to_csv('shared/figures/top50_consecutive_runners.csv',index=False)
print('updated consecutive')

#%% tourism table

upr = df.parkrunner.value_counts()
upr=upr[upr>20]
tourism=[]
for p,c in upr.items():
    listofpr = list(df[df.parkrunner==p].parkrun.unique())
    if len(listofpr)>1:
        home=df[df.parkrunner==p].parkrun.value_counts().idxmax()
        tourism.append({'parkrunner':p,'home_parkrun':home, \
                        'total_us_runs':c,'n_different_parkrun':len(listofpr)})
        print(p,c,len(listofpr))
tourism = pandas.DataFrame.from_dict(tourism)
tourism = tourism.sort_values('n_different_parkrun',ascending=False).iloc[:50,:]
tourism['rank']=arange(1,50+1)
tourism.to_csv('shared/figures/top50_tourists.csv',index=False)

#%%
