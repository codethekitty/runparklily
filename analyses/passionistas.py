#%% passionistas
passionistas=[]
for pr in df.parkrun.unique():
    thisparkrun = df[df.parkrun==pr]
    otherparkrun = df[df.parkrun!=pr]
    parkrunner_list = thisparkrun.parkrunner.value_counts()
    if (pr.find('Bear Creek')>-1)|(pr.find('Third')>-1):
        crit=0
    else:
        crit=5
    parkrunner_list = parkrunner_list[parkrunner_list>crit]
    count=0
    for p,i in parkrunner_list.items():
        check = sum(otherparkrun.parkrunner==p)
        if not bool(check):
            tprs = thisparkrun[thisparkrun.parkrunner==p].nprs.values
            tprs = max([int(x[:x.find('parkrun')-1]) for x in tprs])
            iprs = sum(thisparkrun.parkrunner==p)
            if iprs==tprs:
                passionistas.append({'parkrun':pr,'runner':p,'count':i})
                print(pr,p,i)
                count+=1
                if count>10:
                    break

#%% get top 3
P=pandas.DataFrame.from_dict(passionistas)
for pr in P.parkrun.unique():
    top3 = P[P.parkrun==pr].sort_values(by='count',ascending=False).iloc[:3,:]
    maxevent = max(df[df.parkrun==pr].event)
    top3['parkrun_max']=maxevent
    if pr==P.parkrun.unique()[0]:
        P2=top3
    else:
        P2=pandas.concat((P2,top3))
        
#%% plot
cc=rcParams['axes.prop_cycle'].by_key()['color']
cc*=5
mm = dict(zip(df.parkrun.unique(),arange(len(df.parkrun.unique()))))
P3=P2.iloc[::-1,:].reset_index().iloc[:,1:]
colorcode = P3.parkrun.map(mm)
P3['color']=colorcode
figure(figsize=(10,30))
for i,j in P3.iterrows():
    barh(i,j['count'],facecolor=cc[j['color']])
    plot((j['count'],j['parkrun_max']),[i,i],color=cc[j['color']])
#    plot(j['parkrun_max'],i,'o',color=cc[j['color']])
    text(j['parkrun_max']+5,i,j['runner'],ha='left',va='center',color=cc[j['color']])
    text(j['count']/2,i,'%d'%(j['count']),ha='center',va='center',color='w',fontsize=9)
xt=arange(1,len(P3),3)
xtl=[x[:x.find('parkrun')-1] for x in df.parkrun.unique()[::-1]]
yticks(xt,xtl)
ylim(-1,len(P3))
title('Top 3 Passionistas of each parkrun')
fn = datetime.datetime.now().strftime('%Y.%m.%d')
tt='(updated %s)'%(fn)
title(tt,fontweight='normal',fontsize=10,loc='right')
xlabel('# Events')
       
savefig('shared/figures/passionistas.png',dpi=300,bbox_inches='tight')

#%%
P2=P[P.parkrun.str.find('Lillie')>-1]