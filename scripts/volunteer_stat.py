from pylab import *
import import_data,pandas
df = import_data.import_result()
df2 = import_data.import_volunteer()

#%% find lillie v
cc=rcParams['axes.prop_cycle'].by_key()['color']

dfcount=df2.volunteer.value_counts()
dfcount=dfcount[dfcount>0]
xlab=dfcount.index.values
y2=[]
for n in xlab:
    y2.append(sum(df.parkrunner==n))
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
#savefig('../../volunteer_rank.png',dpi=150,bbox_inches='tight')