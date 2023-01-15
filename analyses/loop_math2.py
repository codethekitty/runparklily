from pylab import *

#%%
d_preloop = 0.56
d_loop = 0.84
d_loop2 = 0.80
d_afterloop = 0.08

d_total = d_preloop + d_loop*2 + d_loop2 + d_afterloop

#%% test path 2
r = d_loop/4
step = 0.001

x1 = arange(0,d_preloop,step)
y1 = zeros(len(x1))
y2 = arange(0,r,step)
x2 = d_preloop*ones(len(y2))
x3 = arange(d_preloop,d_preloop+r,step)
y3 = r*ones(len(x2))
y4 = arange(r,0,-step)
x4 = (d_preloop+r)*ones(len(y4))
x5 = arange(d_preloop+r,d_preloop,-step)
y5 = zeros(len(x5))
x55 = arange(d_preloop+r,d_preloop+(d_loop-d_loop2),-step)
y55 = zeros(len(x55))
y6 = arange(step,-d_afterloop,-step)
x6 = (d_preloop+(d_loop-d_loop2))*ones(len(y6))



X=hstack((x1,x2,x3,x4,x5,x2,x3,x4,x5,x2,x3,x4,x55,x6))
Y=hstack((y1,y2,y3,y4,y5,y2,y3,y4,y5,y2,y3,y4,y55,y6))


figure(figsize=(4,4))
plot(X,Y,'o-',mfc='w',ms=3)
xlim(-0.1,0.9)
ylim(-0.1-0.3,0.9-0.3)
savefig('mm.pdf')
# #
figure(figsize=(4,2))
plot(sqrt(diff(X)**2+diff(Y)**2),'o-')
ylim(0,step*2)

posmat = vstack((X,Y)).T

#%% ignore
import numpy.random as random

pr=24
split=3
dt=step
vpace=pr/d_total


# velocity function
trajectory = linspace(vpace,vpace+split,len(posmat))
phase=3
v_all = trajectory + cos(linspace(0,pi*phase*2,len(posmat)))/2 + random.normal(0,0.2,len(posmat)) #constant changing split
#sin(linspace(0,pi*5,100)+random.normal(0,1,100))

v_new=v_all
mf=20 #moving filter
for i in range(len(v_all)):
    if i/mf==round(i/mf):
        v_new[i]=v_all[i]
    else:
        v_new[i]=v_all[i-1]
v_all=v_new

# position function
tpos=empty(len(posmat))
x=0
for i in range(len(posmat)):
    v = v_all[i]
    x+=v*dt
    tpos[i]=x
subplot(211)
plot(tpos,X)
plot(tpos,Y)
subplot(212)
plot(linspace(0,d_total,len(posmat)),v_all)
plot(linspace(0,d_total,len(posmat)),trajectory)




#%% p
pr = [22.5,57.5] #min

tel=[]
for p in pr:
    tstep = p/d_total*step # (min/mile) * step_mile = t
    tel.append(arange(0,len(posmat))*tstep)

ix = tel[1]<min(pr)
#plot(tel[0],Y,'r',ms=2)
#plot(tel[0],X,'b',ms=2)
#plot(tel[1][ix],Y[ix],'rs',ms=2)
#plot(tel[1][ix],X[ix],'bs',ms=2)
##xlim(0,min(pr))
#
###%%
#plot(tel[0],Y,'r',ms=2)
#plot(tel[1][ix],Y[ix],'rs',ms=2)

timebin = linspace(0,min(pr),5000)
timebin = timebin[1:]
newT=[]
for t in timebin:
    ix2 = argmin(abs(tel[0]-t))
#    plot(tel[0][ix2],Y[ix2],'o')
    ix3 = argmin(abs(tel[1][ix]-t))
#    plot(tel[1][ix][ix3],Y[ix][ix3],'o')
    newT.append([t,X[ix2],Y[ix2],X[ix][ix3],Y[ix][ix3]])
newT=array(newT)
ix = (newT[:,1]==newT[:,3]) & (newT[:,2]==newT[:,4])
ix[:100]=False

scs=['k','b','b','r','r']
for i in range(1,5):
    plot(newT[:,0],newT[:,i],'-',color=scs[i])
    plot(newT[ix,0],newT[ix,i],'ko')
    
ax=gca()
ax.axis('off')
savefig('lake0.pdf',dpi=150,bbox_inches='tight')

    
figure(figsize=(7,3))
plot(X,Y,'s',ms=1)
# xlim(array((-0.4,0.3))+0.3)
# ylim(array((-0.4,0.3))-0.05)
meet=newT[ix,:]
meet[:,0]=around(meet[:,0],1)

plot(0,0,'ks',ms=10,mfc='w')
text(0.0,0.03,'start')
text(0.63,-0.08,'finish')
plot(d_preloop+(d_loop-d_loop2),-d_afterloop,'ks',ms=10)



a = unique(meet[:,0])
if any(diff(a)<1):
    a=a[where(diff(a))[0]]
for i in a:
    ix=where(meet[:,0]==i)[0][0]
    ss=str(meet[ix,0])
    ss1=ss[:ss.find('.')]
    ss2=str(round(int(ss[ss.find('.')+1:])/10*60))
    if len(ss2)==1:
        ss2='0'+ss2
    plot(meet[ix,1],meet[ix,2],'o',ms=10,label=ss1+':'+ss2)
xticks([])
yticks([])
ax=gca()
ax.axis('off')
#plot(0.22,0,'o',ms=10)
#text(0.24,0.025,'roundabout')

savefig('lake1.pdf',dpi=150,bbox_inches='tight')




#%%
#min
def t_meet(t1,t2):
    pr=list(sort([t1,t2]))
    tel=[]
    for p in pr:
        tstep = p/d_total*step # (min/mile) * step_mile = t
        tel.append(arange(0,len(posmat))*tstep)
    
    ix = tel[1]<min(pr)
    
    timebin = linspace(0,min(pr),5000)
    timebin = timebin[1:]
    newT=[]
    for t in timebin:
        ix2 = argmin(abs(tel[0]-t))
        ix3 = argmin(abs(tel[1][ix]-t))
        newT.append([t,X[ix2],Y[ix2],X[ix][ix3],Y[ix][ix3]])
    newT=array(newT)
    ix = (newT[:,1]==newT[:,3]) & (newT[:,2]==newT[:,4])
    ix[:100]=False
    
    
    meet=newT[ix,:]
    meet[:,0]=around(meet[:,0],1)
    
    a = unique(meet[:,0])
    if any(diff(a)<1):
        a=a[where(diff(a))[0]]
    for i in a:
        ix=where(meet[:,0]==i)[0][0]
    N=len(a)
    return N

#%%
P = arange(17,61,1)
M = zeros((len(P),len(P)))
for i,t1 in enumerate(P):
    for j,t2 in enumerate(P):
        if t1==t2:
            M[i,j]=-1
        else:
            M[i,j]=t_meet(t1,t2)
            print(i,j)

#%%
figure(figsize=(5,5))
pcolor(P,P,M)       

text(21,50,'2',fontsize=16)
text(50,21,'2',fontsize=16)
text(24,45,'1',fontsize=16)
text(45,24,'1',fontsize=16)
text(19,56,'1',fontsize=16)
text(56,19,'1',fontsize=16)
text(36,30,'0',fontsize=16)
text(30,36,'0',fontsize=16)
xlabel('Finish time (min)')
ylabel('Finish time (min)')

savefig('pcolor.png',dpi=150,bbox_inches='tight')
