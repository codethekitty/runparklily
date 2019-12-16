#%%
Dall = df[df.parkrun=='Lillie parkrun, Ann Arbor']
D=Dall    
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


#% name plotting

import matplotlib.patches as patches
from numpy.matlib import repmat
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