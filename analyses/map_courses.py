from pylab import *
import os,glob,pandas

#%%
cc=rcParams['axes.prop_cycle'].by_key()['color']

folder = 'runparklily\\data\\kml'
ff = glob.glob(os.path.join(folder,'Lillie*'))[0]
f=open(ff)
s=f.read()
f.close()
start=s.find('<coordinates>')
fin=s.find('</coordinates>')
m=s[start+len('<coordinates>'):fin].split()
m=array([[float(y) for y in x.split(',')] for x in m])[:,:-1]
start=s.find('<Point>')
p=s[start:].split()
for i in p:
    if i[0]!='<':
        break
o=array([float(x) for x in i.split(',')])[:-1]
coor=vstack((m[:,0]-o[0],m[:,1]-o[1])).T

plot(coor[:,0],coor[:,1],lw=3,c=cc[1])
plot(0,0,'*',ms=14,c=cc[4])

xlim(array((min(coor[:,0]),max(coor[:,0])))*1.05)
yl=array((min(coor[:,1]),max(coor[:,1])))
ylim(yl*2.3-0.001)
xticks([])
yticks([])  
ax=gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)     

savefig(r'C:\Users\calvinwu\Google Drive\transfer folder\p1.png',dpi=150,bbox_inches='tight')

#%%
ff = glob.glob(os.path.join(folder,'Livoni*'))[0]
f=open(ff)
s=f.read()
f.close()
start=s.find('<coordinates>')
fin=s.find('</coordinates>')
m=s[start+len('<coordinates>'):fin].split()
m=array([[float(y) for y in x.split(',')] for x in m])[:,:-1]
start=s.find('<Point>')
p=s[start:].split()
for i in p:
    if i[0]!='<':
        break
o=array([float(x) for x in i.split(',')])[:-1]
coor=vstack((m[:,0]-o[0],m[:,1]-o[1])).T

plot(coor[:,0],coor[:,1],lw=3,c=cc[1])
plot(0,0,'*',ms=14,c=cc[4])

# xlim(array((min(coor[:,0]),max(coor[:,0])))*2-0.003)
# yl=array((min(coor[:,1]),max(coor[:,1])))
# ylim(yl*1.05)
xticks([])
yticks([])  
ax=gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)     

# savefig(r'C:\Users\calvinwu\Google Drive\transfer folder\p2.png',dpi=150,bbox_inches='tight')

#%%
folder = 'runparklily\\data\\kml'
files = glob.glob(os.path.join(folder,'*'))

gps={}
cc=rcParams['axes.prop_cycle'].by_key()['color']*5
figure(figsize=[12,8])
for ni,n in enumerate(files):
    
    f=open(n)
    s=f.read()
    f.close()
 
    start=s.find('<coordinates>')
    fin=s.find('</coordinates>')
    m=s[start+len('<coordinates>'):fin].split()
    m=array([[float(y) for y in x.split(',')] for x in m])[:,:-1]


    if len(m)==1:
        o=m
        s=s[fin:]
        start=s.find('<coordinates>')
        s=s[start+len('<coordinates>'):]
        fin=s.find('</coordinates>')
        m=s[:fin].split()
        m=array([[float(y) for y in x.split(',')] for x in m])[:,:-1]
    else:
        start=s.find('<Point>')
        p=s[start:].split()
        if os.path.basename(n).find('Himmel')<0:
            for i in p:
                if i[0]!='<':
                    break
            o=array([float(x) for x in i.split(',')])[:-1]
        else:
            o=m[argmax(m[:,1])]
            
    if len(o)==1:
        o=o[0]
        
    coor=vstack((m[:,0]-o[0],m[:,1]-o[1])).T
    plot(coor[:,0],coor[:,1],color=cc[ni])

    
    label=os.path.basename(n)[:-4].replace('parkrun','').rstrip()
    gps[label]=coor

    xy=argmax((coor[:,0]**2+coor[:,1]**2)**0.5)
    x,y=coor[xy,:]
    text(x,y,label,color=cc[ni])
xticks([])
yticks([])  
ax=gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)    
plot(0,0,'*',ms=10,c='k')
 
# savefig(r'C:\Users\calvinwu\Google Drive\transfer folder\p3.png',dpi=150,bbox_inches='tight')


#%% summary
summary = 'runparklily\\data\\courses.csv'
df=pandas.read_csv(summary)
from matplotlib import gridspec
gs=gridspec.GridSpec(1,2)
figure(figsize=[8,2.5],dpi=150)

for s in (0,1):
    if s==0:
        X,Y=df['loop'],df['out and back']
    else:
        X,Y=df['loop rep'],df['out and back rep']
    subplot(gs[s])
    h,xedge,yedge=histogram2d(X,Y,bins=(max(X)+1,max(Y)+1))
    x,y = meshgrid(arange(max(X)+1),arange(max(Y)+1))
    z=zeros(len(x.ravel()))
    c=0
    for i,j in zip(x.ravel(),y.ravel()):
        z[c]=h[i,j]
        c+=1
    scatter(x.ravel(),y.ravel(),s=z*30,c=z,cmap='viridis_r')
    xlim(min(X)-0.5,max(X)+0.5)
    ylim(min(Y)-0.5,max(Y)+0.5)
    colorbar(ticks=arange(0,18,2))
    
    if s==1:
        text(4,1,'Lillie',fontsize=8,rotation=45)
        text(6,0,'Lillie w',fontsize=8,rotation=45)
        text(1,1,'Livonia',fontsize=8,rotation=45)
        text(2,5,'Livonia w',fontsize=8,rotation=45,ha='right',va='top')
        ylabel('out and back')
        xlabel('loops')
    else:
        text(2,1,'Lillie',fontsize=8,rotation=45)
        text(1,1,'Livonia',fontsize=8,rotation=45)
        ylabel('lines')
        xlabel('circles')


# savefig(r'C:\Users\calvinwu\Google Drive\transfer folder\p4.png',dpi=150,bbox_inches='tight')

#%%

coor=gps[list(gps)[-1]]

plot(coor[:,0],coor[:,1],lw=3,c=cc[1])
plot(0,0,'*',ms=14,c=cc[4])
# xlim(array((min(coor[:,0]),max(coor[:,0])))*2-0.003)
# yl=array((min(coor[:,1]),max(coor[:,1])))
# ylim(yl*1.05)
xticks([])
yticks([])  
ax=gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)     

savefig(r'C:\Users\calvinwu\Google Drive\transfer folder\p2.png',dpi=150,bbox_inches='tight')

