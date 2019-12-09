#%%
from matplotlib.gridspec import GridSpec

data_all=df[df.parkrun=='Lillie parkrun, Ann Arbor']
data2 = data_all.parkrunner.value_counts()

parkrunners=list(data2.index)

L=empty((max(data2),len(parkrunners)))
L[:]=nan
c=-1
for n,p in zip(data2,parkrunners):
    d=data_all[data_all.parkrunner==p]
    c+=1
    for i,r in d.iterrows():
        timestr = r.time
        if len(timestr)<=5:
            t = datetime.datetime.strptime(r.time,'%M:%S')
            L[r.event-1,c]=t.minute+t.second/60
        else:
            t = datetime.datetime.strptime(r.time,'%H:%M:%S')
            L[r.event-1,c]=t.hour*60+t.minute+t.second/60
            
#%
fig,(cax,ax)=subplots(nrows=2,figsize=(6.5,65),gridspec_kw={'height_ratios':[0.002,1]})
a=ax.pcolormesh(L.T[::-1,:])
ts=arange(18,42,4)
tlabel=[str(x) for x in list(ts)[:-1]]
tlabel.append('>'+str(list(ts)[-1]))
cbar = colorbar(a,cax=cax,orientation="horizontal",ticks=ts)
a.set_clim(18,38)
cax.set_xlabel('Finish time (min)')
cax.set_xticklabels(tlabel)
tight_layout()
initial=[x[0]+' '+x[x.find(' ')+1] for x in parkrunners]
ax.set_yticks(arange(len(parkrunners))+0.5)
ax.set_yticklabels(initial[::-1],fontsize=7)
ax.set_xlabel('Event #')
              
              
fn = datetime.datetime.now().strftime('%Y_%m_%d')
savefig('shared/figures/event_plot_'+fn+'.png',dpi=300,bbox_inches='tight')
