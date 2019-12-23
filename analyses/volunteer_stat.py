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
fn = datetime.datetime.now().strftime('%Y_%m_%d')
tt='(updated %s)'%(fn)
title(tt,fontweight='normal',fontsize=10,loc='right')

savefig('shared/figures/volunteer_stat1.png',dpi=300,bbox_inches='tight')



#%% get task detail from npy

sdir='shared/data/raw_data/volunteer_data'

df3 = df2[df2.parkrun=='Lillie parkrun, Ann Arbor']
dfcount=df3.volunteer.value_counts()
dfcount=dfcount[dfcount>2]
result={}
task_temp=[]
names=[]
for v in dfcount.index:
    barcode = 'a'+df3[df3.volunteer==v].barcode.values[0]+'.npy'
    ll=load(os.path.join(sdir,barcode),allow_pickle=True).item()['data']
    result[v]=[]
    for i in ll:
        result[v].extend([i[1]]*int(i[2]))
        task_temp.append(i[1])
        
    name = v[:v.find(' ')+2]
    if name=='T. C':
        name='T. Charles Y'
    if name=='Torsten J':
        name='Torsten Y'
    if name=='Aldus K':
        name='Aldus Y'
    names.append(name)

#%%
u=unique(task_temp)
u_order = hstack((u[17],u[2],u[22],u[4],u[15],u[1],u[7],u[20],u[0],u[6],u[5],u[21],u[10] \
        ,u[9],u[19],u[11],u[12],u[13],u[8],u[14],u[3],u[16],u[18]))
u_ind = array([False,True,True,True,True,True,True,False,False,True, \
               True,True,True,False,True,True,True,True,True,True,True,True,True])
map_val = dict(zip(u_order,arange(len(u))))
M=zeros((len(result),len(u_order)))
for i,(k,v) in enumerate(result.items()):
    d=pandas.Series(v).map(map_val).value_counts()
    for j in d.iteritems():
        M[i,j[0]]=j[1]
#%%
from matplotlib import gridspec

figure(figsize=(8,11))
gs=gridspec.GridSpec(1,2,width_ratios=(1,10))

ax=subplot(gs[0])
barh(arange(len(dfcount))+0.5,-dfcount[::-1],0.7,facecolor=matplotlib.cm.get_cmap('viridis')(0))
ylim(0,len(dfcount))
xticks(arange(-50,25,25),[50,25,0])
xlim(-55,0)
yticks([])
xlabel('Total count')

#plot(-dfcount[::-1],arange(len(dfcount))+0.5,'ko-')
#ylim(0,len(dfcount))
#xticks(arange(-50,25,25),[50,25,0])
#xlim(-55,0)
#yticks([])
#xlabel('Total v')
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)

subplot(gs[1])
setm=30
MT=clip(M,0,setm)
pcolormesh(flipud(MT))
xticks(arange(len(u))+0.5,u_order,rotation=90)
yticks(arange(len(result))+0.5,list(names)[::-1])
ylim(0,len(dfcount))
cc=colorbar(fraction=0.03,aspect=55)
tt=arange(0,setm+5,5)
cc.set_ticks(tt)
cc.set_ticklabels(hstack((tt[:-1],str(setm)+'+')))
tight_layout()

fn = datetime.datetime.now().strftime('%Y.%m.%d')
tt='(updated %s)'%(fn)
title(tt,fontweight='normal',fontsize=10,loc='right')

savefig('shared/figures/volunteer_stat2.png',dpi=300,bbox_inches='tight')

