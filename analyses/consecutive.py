from matplotlib import gridspec
#%
parkrunlist = list(df.parkrun.unique())
result=[]
for p in parkrunlist:
    leaders = df[df.parkrun==p].parkrunner.value_counts()
    leaders=leaders[leaders>max(leaders)/10]
    leaders=leaders.index
    print(len(leaders),df[df.parkrun==p].event.max())
    most_conseq_parkrun=[]
    for leader in leaders:
        a=sort(df[(df.parkrun==p) & (df.parkrunner==leader)].event.values)
        if all(diff(a)>0):
            count=1
            last_value=a[0]
            countS=[]
            for i in a[1:]:
                if i==last_value+1:
                    count+=1
                else:
                    countS.append(count)
                    count=1
                last_value=i
            if len(countS)>0:
                most_conseq=max(countS)
            else:
                most_conseq=len(a)
            conseq_loc=[]
            for i in range(len(a)):
                if len(a[i:i+most_conseq])==most_conseq:
                    if std(diff(a[i:i+most_conseq]))==0:
                        conseq_loc=a[i:i+most_conseq]
            cur=df[df.parkrun==p].event.max()
            # most_conseq_parkrun.append(most_conseq)
        # if most_conseq>=max(most_conseq_parkrun):
            if most_conseq>2:
                result.append({'parkrun':p,'leader':leader,'most_conseq':most_conseq,'events':conseq_loc,'current':cur})
                print(p,leader,most_conseq)
                    

scott=pandas.DataFrame.from_dict(result)

#%%
for i,p in enumerate(scott.parkrun.unique()):
    pp=scott[scott.parkrun==p].sort_values(by='most_conseq',ascending=False)
    pp=pp.iloc[:3,:]
    if i==0:
        P2=pp
    else:
        P2=pandas.concat((P2,pp))


#%%
cc=rcParams['axes.prop_cycle'].by_key()['color']
cc=cc*10

for i,r in P2.iterrows():
    eventplot(r.events,lineoffsets=-i,color=cc[i],linelengths=0.8)
    plot(2*[r.current],array([-0.5,0.5])-i,'-',color=cc[i],lw=1)
    plot([0,r.current],[-i,-i],'-',color=cc[i],lw=1)
    text(r.current+5,-i,'%s (%d)'%(r.leader,r.most_conseq),color=cc[i],ha='left',va='center')
# yticks(arange(-i,1,1),[x[:x.find('parkrun')-1] for x in scott2.parkrun[::-1]])
# ylim(-i-1,1)
# xlim(0,440)
# xlabel('Event #')
# title('Most consecutive runner at each parkrun')

# fn = datetime.datetime.now().strftime('%Y.%m.%d')
# tt='(updated %s)'%(fn)
# title(tt,fontweight='normal',fontsize=10,loc='right')


# savefig('shared/figures/consecutive_run1.png',dpi=300,bbox_inches='tight')


#%%


cc=rcParams['axes.prop_cycle'].by_key()['color']
cc=cc*5

figure(figsize=(14,8))

gs=gridspec.GridSpec(2,1,height_ratios=(5,4))

subplot(gs[0])
scott2 = scott.sort_values(by='most_conseq',ascending=False).reset_index()
scott2=scott2.iloc[:-1,:]
i=0
t=[]
for j,r in scott2.iterrows():
    if (r.events[0]==1):
#        eventplot(r.events,lineoffsets=-i,color=cc[i],linelengths=0.8)
        barh(-i,max(r.events),facecolor=cc[i],height=0.5)
        plot(2*[r.current],array([-0.5,0.5])-i,'-',color=cc[i],lw=1)
        plot([0,r.current],[-i,-i],'-',color=cc[i],lw=1)
        if r.current==r.events[-1]:
            fw='bold'
        else:
            fw='normal'
        if r.current<75:
            xpos=r.current+2
        else:
            xpos=75
        text(xpos,-i,'%s (%d)'%(r.leader,r.most_conseq),color=cc[i],ha='left',va='center',fontweight=fw)
        i+=1
        t.append(r.parkrun[:r.parkrun.find('parkrun')-1])
yticks(arange(-i+1,1,1),t[::-1])
ylim(-i,1)
xlim(0,100)
xlabel('Event #')
title('Most consecutive runner since event #1')

fn = datetime.datetime.now().strftime('%Y.%m.%d')
tt='(updated %s)'%(fn)
title(tt,fontweight='normal',fontsize=10,loc='right')

subplot(gs[1])
scott2 = scott.sort_values(by='most_conseq',ascending=False).reset_index()
scott2=scott2.iloc[:-1,:]
i=0
t=[]
for j,r in scott2.iterrows():
    if (max(r.events)==r.current)&(len(r.events)>2):
        eventplot(r.events[:-1],lineoffsets=-i,color=cc[i],linelengths=0.45,linewidth=7)
        plot(2*[r.current],array([-0.5,0.5])-i,'-',color=cc[i],lw=1)
        plot([0,r.current],[-i,-i],'-',color=cc[i],lw=1)
        if r.events[0]==1:
            fw='bold'
        else:
            fw='normal'
        text(r.current+2,-i,'%s (%d)'%(r.leader,r.most_conseq),color=cc[i],ha='left',va='center',fontweight=fw)
        i+=1
        t.append(r.parkrun[:r.parkrun.find('parkrun')-1])
yticks(arange(-i+1,1,1),t[::-1])
ylim(-i,1)
xlim(0,250)
xlabel('Event #')
title('Most consecutive runner still in progress')
      
tight_layout()
      

savefig('shared/figures/consecutive_run2.png',dpi=300,bbox_inches='tight')




