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


#%% volunteer team league table

Dall = df[df.parkrun=='Lillie parkrun, Ann Arbor']
Dvol = df2[df2.parkrun=='Lillie parkrun, Ann Arbor']
gs = gridspec.GridSpec(2,1,height_ratios=(1,2))

figure(figsize=(16,8))

firstnames = [x.split(' ') for x in Dvol.volunteer]
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
    cc=len(unique(Dvol[ix].volunteer))
    if cc>1:
        Dsub={}
        for n in unique(Dvol[ix].volunteer):
            D2=Dvol[ix][Dvol[ix].volunteer==n]            
            Dsub[n]=len(D2)
        stat.append({'fname':u,'count':cc,'total_runs':sum(ix),'detail':Dsub})
stat=pandas.DataFrame.from_dict(stat)
stat=stat.sort_values(by='total_runs',ascending=False).reset_index().drop(columns='index')
stat=stat[(stat.total_runs/stat['count'])>1].reset_index().drop(columns='index')

cc=rcParams['axes.prop_cycle'].by_key()['color']

ax = subplot(gs[0])
xt=[]
for i,j in stat.iterrows():
    v=0
    for k,v1 in j.detail.items():
        rect = patches.Rectangle((v,len(stat)-i-0.5),v1,1,linewidth=1,edgecolor='w',facecolor=cc[i])
        if v1>1:
            ln=k.split(' ')[-1]
            text(mean([v,v+v1]),len(stat)-i,ln,ha='center',va='center',fontsize=12-1.5*len(ln)/v1,color='w')
        v+=v1
        ax.add_patch(rect)
    xt.append(j.fname+': '+str(j['count']))
ylim(0,len(stat)+1)
xlim(0,stat.total_runs[0]+1)
yticks(arange(len(xt))+1,xt[::-1],ha='right')
ax.set_xlabel('Total Volunteering',fontsize=12)
ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top') 
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ylabel('(by first name)')

fn = datetime.datetime.now().strftime('%Y.%m.%d')
tt='(updated %s)'%(fn)
title(tt,fontweight='normal',fontsize=10,loc='right')

firstnames = [x.split(' ') for x in Dvol.volunteer]
N=[]
for i in firstnames:
    n=i[-1]
    N.append(n)
stat=[]
for u in unique(N):
    ix=isin(N,u)
    cc=len(unique(Dvol[ix].volunteer))
    if cc>1:
        Dsub={}
        for n in unique(Dvol[ix].volunteer):
            D2=Dvol[ix][Dvol[ix].volunteer==n]            
            Dsub[n]=len(D2)
        stat.append({'fname':u,'count':cc,'total_runs':sum(ix),'detail':Dsub})
stat=pandas.DataFrame.from_dict(stat)
stat=stat.sort_values(by='total_runs',ascending=False).reset_index().drop(columns='index')
stat=stat[(stat.total_runs/stat['count'])>1].reset_index().drop(columns='index')


cc=rcParams['axes.prop_cycle'].by_key()['color']
cc+=cc

ax=subplot(gs[1])
xt=[]
for i,j in stat.iterrows():
    v=0
    for k,v1 in j.detail.items():
        rect = patches.Rectangle((v,len(stat)-i-0.5),v1,1,linewidth=1,edgecolor='w',facecolor=cc[i])
        if v1>1:
            ln=k.split(' ')[0]
            if ln=='T.':
                ln='Charles'
            text(mean([v,v+v1]),len(stat)-i,ln,ha='center',va='center',fontsize=12-1.5*len(ln)/v1,color='w')
        v+=v1
        ax.add_patch(rect)
    xt.append(j.fname+': '+str(j['count']))
ylim(0,len(stat)+1)
xlim(0,stat.total_runs[0]+1)
yticks(arange(len(xt))+1,xt[::-1],ha='right')
ax.set_xlabel('Total Volunteering',fontsize=12)
ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top') 
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ylabel('(by last name)')

tight_layout()

savefig('shared/figures/name_team_volunteer.png',dpi=300,bbox_inches='tight')
print('updated volunteer league table (team)')

#%% volunteer individual league table

df3 = df2[df2.parkrun=='Lillie parkrun, Ann Arbor']
df4 = df[df.parkrun=='Lillie parkrun, Ann Arbor']

cc=rcParams['axes.prop_cycle'].by_key()['color']

dfcount=df3.volunteer.value_counts()
dfcount=dfcount[dfcount>0]
xlab=dfcount.index.values
y2=[]
for n in xlab:
    y2.append(sum(df4.parkrunner==n))
ix=[array(y2)>3]
y=dfcount.values[ix]
x=arange(len(y))
y2=array(y2)[ix]
xlab=xlab[ix]
fig,ax=subplots(figsize=[14,16])
ax.barh(-x,y,facecolor=cc[4])
ax.barh(-x,-array(y2),facecolor=cc[1])
ax.set_ylim(min(-x)-1,max(-x)+1)
ax.set_xticklabels([int(x) for x in abs(ax.get_xticks())])
ax.set_yticks([])
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
for n,xp,right,left in zip(xlab,-x,y,-array(y2)):
    name = n[:n.find(' ')+2]
    if name=='T. C':
        name='T. Charles Y'
    if name=='Torsten J':
        name='Torsten Y'
    if name=='Aldus K':
        name='Aldus Y'
    if (right-left)>4:
        text((right+left)/2,xp,name,ha='center',va='center',color='w',fontsize=10)
    else:
        text(2.5,xp,name,ha='left',va='center',color='k',fontsize=10)
text(-30,2.5,'# Runs',ha='center',fontsize=11,color=cc[1],fontweight='bold')
text(25,2.5,'# Volunteering',ha='center',fontsize=11,color=cc[4],fontweight='bold')
ax.xaxis.set_ticks_position('top')
fn = datetime.datetime.now().strftime('%Y.%m.%d')
tt='(updated %s)'%(fn)
title(tt,fontweight='normal',fontsize=10,loc='right')

savefig('shared/figures/volunteer_stat1.png',dpi=300,bbox_inches='tight')
print('updated volunteer league table (individual)')

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
    for p,i in parkrunner_list.items():
        check = sum(otherparkrun.parkrunner==p)
        if not bool(check):
            tprs = thisparkrun[thisparkrun.parkrunner==p].nprs.values
            tprs = max([int(x[:x.find('parkrun')-1]) for x in tprs])
            iprs = sum(thisparkrun.parkrunner==p)
            if iprs==tprs:
                passionistas.append({'parkrun':pr,'runner':p,'count':i})
                print(pr,p,i)
                count+=1
                if count>10:
                    break

#% get top 3
P=pandas.DataFrame.from_dict(passionistas)
for pr in P.parkrun.unique():
    top3 = P[P.parkrun==pr].sort_values(by='count',ascending=False).iloc[:3,:]
    maxevent = max(df[df.parkrun==pr].event)
    top3['parkrun_max']=maxevent
    if pr==P.parkrun.unique()[0]:
        P2=top3
    else:
        P2=pandas.concat((P2,top3))
        
#% plot
cc=rcParams['axes.prop_cycle'].by_key()['color']
cc*=5
mm = dict(zip(df.parkrun.unique(),arange(len(df.parkrun.unique()))))
P3=P2.iloc[::-1,:].reset_index().iloc[:,1:]
colorcode = P3.parkrun.map(mm)
P3['color']=colorcode
figure(figsize=(10,30))
for i,j in P3.iterrows():
    barh(i,j['count'],facecolor=cc[j['color']])
    plot((j['count'],j['parkrun_max']),[i,i],color=cc[j['color']])
#    plot(j['parkrun_max'],i,'o',color=cc[j['color']])
    text(j['parkrun_max']+5,i,j['runner'],ha='left',va='center',color=cc[j['color']])
    text(j['count']/2,i,'%d'%(j['count']),ha='center',va='center',color='w',fontsize=9)
xt=arange(1,len(P3),3)
xtl=[x[:x.find('parkrun')-1] for x in df.parkrun.unique()[::-1]]
yticks(xt,xtl)
ylim(-1,len(P3))
title('Top 3 Passionistas of each parkrun')
fn = datetime.datetime.now().strftime('%Y.%m.%d')
tt='(updated %s)'%(fn)
title(tt,fontweight='normal',fontsize=10,loc='right')
xlabel('# Events')
       
savefig('shared/figures/passionistas.png',dpi=300,bbox_inches='tight')
print('updated passionistas')
