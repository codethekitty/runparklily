Dall = df[df.parkrun=='Lillie parkrun, Ann Arbor']
Dvol = df2[df2.parkrun=='Lillie parkrun, Ann Arbor']

#%% first name team


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

# name plotting

import matplotlib.patches as patches
cc=rcParams['axes.prop_cycle'].by_key()['color']

fig, ax = subplots(figsize=(16,3))
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


fn = datetime.datetime.now().strftime('%Y_%m_%d')
savefig('shared/figures/firstnameteam_volunteer_'+fn+'.png',dpi=300,bbox_inches='tight')

#%% last name team


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

#% name plotting

import matplotlib.patches as patches
cc=rcParams['axes.prop_cycle'].by_key()['color']
cc+=cc

fig, ax = subplots(figsize=(16,5))
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


fn = datetime.datetime.now().strftime('%Y_%m_%d')
savefig('shared/figures/lastnameteam_volunteer_'+fn+'.png',dpi=300,bbox_inches='tight')