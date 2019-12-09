#%%
scott_data = df[(df.parkrunner=='Scott REVORD')&(df.parkrun=='Lillie parkrun, Ann Arbor')]
#%%
parkrunlist = list(df.parkrun.unique())
result=[]
for p in parkrunlist:
    l=0
    leader = df[df.parkrun==p].parkrunner.value_counts().index[l]
    a=sort(df[(df.parkrun==p) & (df.parkrunner==leader)].event.values)
    while any(diff(a)==0):
        l+=1
        leader = df[df.parkrun==p].parkrunner.value_counts().index[l]
        a=sort(df[(df.parkrun==p) & (df.parkrunner==leader)].event.values)
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
        most_conseq=last_value
    conseq_loc=[]
    for i in range(len(a)):
        if len(a[i:i+most_conseq])==most_conseq:
            if std(diff(a[i:i+most_conseq]))==0:
                conseq_loc=a[i:i+most_conseq]
    cur=df[df.parkrun==p].event.max()
    result.append({'parkrun':p,'leader':leader,'most_conseq':most_conseq,'events':conseq_loc,'current':cur})
    print(p)

scott=pandas.DataFrame.from_dict(result)

#%%
cc=rcParams['axes.prop_cycle'].by_key()['color']
cc=cc*5

figure(figsize=(14,12))

scott2 = scott.sort_values(by='most_conseq',ascending=False).reset_index()
for i,r in scott2.iterrows():
    eventplot(r.events,lineoffsets=-i,color=cc[i],linelengths=0.8)
    plot(2*[r.current],array([-0.5,0.5])-i,'-',color=cc[i],lw=1)
    plot([0,r.current],[-i,-i],'-',color=cc[i],lw=1)
    text(r.current+5,-i,'%s (%d)'%(r.leader,r.most_conseq),color=cc[i],ha='left',va='center')
yticks(arange(-i,1,1),[x[:x.find('parkrun')-1] for x in scott2.parkrun[::-1]])
ylim(-i-1,1)
xlim(0,400)
xlabel('Event #')
title('Most consecutive parkrunner')

fn = datetime.datetime.now().strftime('%Y_%m_%d')
savefig('shared/figures/scott_leads1_'+fn+'.png',dpi=300,bbox_inches='tight')


#%%


cc=rcParams['axes.prop_cycle'].by_key()['color']
cc=cc*5

figure(figsize=(14,5))
subplot(211)
scott2 = scott.sort_values(by='most_conseq',ascending=False).reset_index()
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
        text(r.current+2,-i,'%s (%d)'%(r.leader,r.most_conseq),color=cc[i],ha='left',va='center',fontweight=fw)
        i+=1
        t.append(r.parkrun[:r.parkrun.find('parkrun')-1])
yticks(arange(-i+1,1,1),t[::-1])
ylim(-i,1)
xlim(0,100)
xlabel('Event #')
title('Most consecutive parkrunner since event #1')

subplot(212)
scott2 = scott.sort_values(by='most_conseq',ascending=False).reset_index()
i=0
t=[]
for j,r in scott2.iterrows():
    if (r.events[-1]==r.current):
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
xlim(0,200)
xlabel('Event #')
title('Most consecutive parkrunner still in progress')
      
tight_layout()
      
      
fn = datetime.datetime.now().strftime('%Y_%m_%d')
savefig('shared/figures/scott_leads2_'+fn+'.png',dpi=300,bbox_inches='tight')



