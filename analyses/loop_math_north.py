from pylab import *
import math,os,glob,pandas

#%%

def eq_meet(x,n):
    y=(6-n)*x/6
    return(y)

x=arange(18,70,0.5)

figure(figsize=(4,4))

cc=rcParams['axes.prop_cycle'].by_key()['color']

for n in range(6):
    y=eq_meet(x,n)
    fill_between(x,y,color=cc[n])
    fill_between(y,x,ones(len(x))*max(x),color=cc[n])
plot(x,x,'-',color='gray')

lx=60
ly=19
theta = math.atan(ly/lx)
r = (lx**2+ly**2)**0.5
s=4
for dtheta in linspace(theta,pi/4,5):
    lx = r*cos(dtheta)
    ly = r*sin(dtheta)
    text(lx+5,ly,str(s),color='w')
    text(ly,lx+5,str(s),color='w')
    s-=1

xlim(min(x),max(x))
ylim(min(x),max(x))
xlabel('Finish time (min)')
ylabel('Finish time (min)')  
    
    
#%% simulation 1v1

fs=1000
ftratio=45/60

theta=linspace(0,2*pi*6,fs)
x,y=cos(theta),sin(theta)
x1,y1=cos(theta*ftratio),sin(theta*ftratio)

figure(figsize=(4,6))
subplot(311)
plot(x)
plot(x1)

subplot(312)
plot(abs(x-x1))
plot(abs(y-y1))

s1=set(where(abs(x-x1)<0.1)[0])
s2=set(where(abs(y-y1)<0.1)[0])

s=s1.intersection(s2)
sc=sort(array(list(s)))

sep=where(diff(sc)!=1)[0]
meet=[]
for i in sep:
    plot(sc[i+1],1,'o')
    print(sc[i+1])
    meet.append(sc[i+1])
    
subplot(313)
plot(x,y,'-')
for c,i in enumerate(meet):
    plot(x[i],y[i],'o')
    text(x[i],y[i],str(int(c)+1))
    
#%% functionize

def loc_meet(tfast,tslow):
    fs=1000
    ftratio=tfast/tslow
    theta=linspace(0,2*pi*6,fs)
    x,y=cos(theta),sin(theta)
    x1,y1=cos(theta*ftratio),sin(theta*ftratio)

    s1=set(where(abs(x-x1)<0.1)[0])
    s2=set(where(abs(y-y1)<0.1)[0])
    s=s1.intersection(s2)
    sc=sort(array(list(s)))
    
    sep=where(diff(sc)!=1)[0]
    meet=[]
    for i in sep:
        meet.append(sc[i+1])
        
    return(array(meet))


#%% past results

from itertools import combinations
from matplotlib import gridspec

folder=r'C:\Users\calvinwu\Google Drive\transfer folder\parkrun_us\shared\data\raw_data\run_data\Lillie parkrun, Ann Arbor'
folder='/Users/catbox/Google Drive/transfer folder/parkrun_us/shared/data/raw_data/run_data/Lillie parkrun, Ann Arbor'
pp=glob.glob(os.path.join(folder,'*.npy'))

figure(figsize=(12,8))
gs=gridspec.GridSpec(2,3)
cc=rcParams['axes.prop_cycle'].by_key()['color']

for sp,ev in zip(range(4),(14,15,57)[::1]):
    if sp>-1:
        events = array([int(os.path.basename(x)[5:-4]) for x in pp])==ev
        data=load(array(pp)[events][0],allow_pickle='True').item()
        
        t=[]
        for k,v in data.items():
            if type(k)==int:
                for i in v:
                    if (i.find(':')>0)&(i.find('PB')==-1):
                        if len(i)<7:
                            t.append(float(i[:i.find(':')])+float(i[i.find(':')+1:])/60)
                            
        t=array(t)
        
        subplot(gs[sp])
        r=1
        meet_point=[]
        for j in range(len(t)):
            l=loc_meet(t[0],t[j])
            if len(l)>0:
                meet_point.extend(l)
        h,b=histogram(array(meet_point),arange(0,1000,2))
        print(sum(h))

        plot((r+h)*cos(b[:-1]/1000*2*pi*6),(r+h)*sin(b[:-1]/1000*2*pi*6),'.-',color=cc[1])
        xlim(-max(h)-2,max(h)+2)
        ylim(-max(h)-2,max(h)+2)
        
        # plot([0,r*max(h+2)],[0,0],'k-')
        # plot([r*max(h+1)]*2,[0,1],'k-')
        # plot([r*max(h+1),r*max(h+1.2)],[1,0.75],'k-')
        # plot([r*max(h+1),r*max(h+0.8)],[1,0.75],'k-')
    
        for r in range(1,max(h)+2):
            x=linspace(0,1,100)
            plot(r*cos(2*pi*x),r*sin(2*pi*x),'k:')
            text(0,r,str(r-1))
        xticks([])
        yticks([])
        title('Event %d (%s): %d runners'%(data['event_number'],data['event_date'],len(t)),fontsize=10)   
    ax=gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
tlist=t

#%%
from numpy import matlib
tlist=sorted(tlist,reverse=True)

figure(figsize=(12.5,2))
X=[]
Y=[]

for c,T in enumerate(tlist):
    step=1/(5/6*1000)*2
    if c==0:
        tmax=T
        theta=matlib.repmat(arange(0,1,step),1,6)[0]
        t_set=linspace(0,T,len(theta))
        tt=t_set
    else:
        step=step*tmax/T
        theta=matlib.repmat(arange(0,1,step),1,6)[0]
        tt=t_set[:len(theta)]
    X.extend(tt)
    Y.extend(theta)

xbin=unique(t_set)
ybin=unique(theta)
H,xedge,yedge=histogram2d(X,Y,bins=(xbin,ybin))
pcolormesh(xedge[:-1],yedge[:-1],H.T,cmap='coolwarm')

xlabel('Time (min)')
ylabel('Location (% lap)')
yticks(arange(0,1,0.2),[int(x) for x in arange(0,1,0.2)*100])
title(str(len(t))+' runners\n(simulation based on transplanted #57 to the north course)',fontsize=10)
colorbar()
clim(0,5)


#%%
D=[]
for ev in pp:
    data=load(ev,allow_pickle='True').item()
    
    t=[]
    for k,v in data.items():
        if type(k)==int:
            for i in v:
                if (i.find(':')>0)&(i.find('PB')==-1):
                    if len(i)<7:
                        t.append(float(i[:i.find(':')])+float(i[i.find(':')+1:])/60)
    X=[]
    Y=[]           
    tlist=array(t)
    tlist=sorted(tlist,reverse=True)

    for c,T in enumerate(tlist):
        step=1/(5/6*1000)*2
        if c==0:
            tmax=T
            theta=matlib.repmat(arange(0,1,step),1,6)[0]
            t_set=linspace(0,T,len(theta))
            tt=t_set
        else:
            step=step*tmax/T
            theta=matlib.repmat(arange(0,1,step),1,6)[0]
            tt=t_set[:len(theta)]
        X.extend(tt)
        Y.extend(theta)
    
    xbin=unique(t_set)
    ybin=unique(theta)
    H,xedge,yedge=histogram2d(X,Y,bins=(xbin,ybin))  
    
    wx,wy=where(H>5)
    widx=where(xbin>3)[0]
    congest = sum(wx>min(widx))
    D.append([len(tlist),congest])
    print(ev)
#%%
figure(figsize=(8,3))
D2=array(D)
D2=D2[argsort(D2[:,0]),:]
plot(D2[:,0],D2[:,1],'ko')
xlabel('Number of finishers')
ylabel('Instances of congestion')

from scipy.optimize import curve_fit
def func(x, a, b):
    return a * exp(b*x)

popt, pcov = curve_fit(func, D2[:,0], D2[:,1],bounds=[0,[0.1,1]])
xnew=linspace(min(D2[:,0]),max(D2[:,0]),500)
plot(xnew, func(xnew, *popt),'r',lw=2)

thry=max(D2[D2[:,0]<40,1])
thrx=xnew[argmin(abs(func(xnew, *popt)-thry))]
xlim(0,100)
ylim(0,205)
plot([0,thrx],[thry,thry],'r:')
plot([thrx,thrx],[0,205],'r:')
text(thrx,100,'threshold: %d'%(thrx),ha='right',va='center')