from datetime import datetime

data=df[df.parkrun=='Lillie parkrun, Ann Arbor']

#%%
b=arange(16,70,2)
AA=zeros(len(b)-1)
BB=AA.copy()
f,ax=subplots(2,1)

for n in (5,10,20,40):
    for i in arange(69,69-n-1,-1):
        T=data[data.event==i].time.values
        A=[]
        for j in T:
            if j.count(':')==1:
                t=float(j[:j.find(':')])+float(j[j.find(':')+1:])/60
            elif j.count(':')==2:
                t=float(j[:j.find(':')])*60+float(j[j.find(':')+1:j.find(':')+3])
            A.append(t)
        y,x=histogram(array(A),b)
        # plot(x[:-1],y,'-')
        
        AA=vstack((AA,y))
        BB=vstack((BB,cumsum(y)))
    AA=AA[1:,:]
    BB=BB[1:,:]
    
    
    # ax[0].errorbar(x[:-1],mean(AA,axis=0),std(AA,axis=0),color='b')
    ax[0].plot(x[:-1],mean(AA,axis=0))
    ax[0].set_ylabel('Count (finished)')
    
    ax[1].plot(x[:-1],mean(BB,axis=0),label=n)
    ax[1].set_xlabel('Finish Time (min)')
    ax[1].set_ylabel('Cumulative count')
    
legend()
