import glob,pandas
#%%
F=glob.glob('shared\\data\\raw_data\\volunteer_data\\*.npy')
vdata={}
for f in F:
    d = load(f,allow_pickle=True).item()
    v = [x[1:] for x in d['data'] if x[0]=='2020']
    if len(v)>0:
        vall=[]
        for i in v:
            if i[0]=='Other':
                i[0]='Run Briefing'
            vall.extend([i[0]]*int(i[1]))
        vdata[d['volunteer']]=vall
vdata.pop('Andrea ZUKOWSKI')
vdata=dict(sorted(vdata.items(),key=lambda item:item[0]))
#%%
v=[]
dummy=[v.extend(x) for x in vdata.values()]
v=unique(v)
order=['Volunteer Co-ordinator','Communications Person','Pre-event Setup', \
       'First Timers Briefing','Run Briefing','Run Director','Timekeeper','Barcode Scanning', \
           'Finish Tokens','Finish Token Support','Token Sorting', \
               'Marshal', 'Pacer (5k only)', 'Photographer','Tail Walker', \
                   'Funnel Manager','Post-event Close Down', \
                       'Results Processor','Run Report Writer']

#%%
figure(figsize=(12,6))
count=0
D=[]
for k,v in vdata.items():
    ar=[where(isin(order,i))[0][0] for i in v]
    h=histogram(array(ar),arange(-0.5,len(order)+1,1))
    D.extend(array(([count]*sum(h[0]>0),where(h[0]>0)[0],h[0][h[0]>0])).T)
    count+=1
D=array(D)
fill_between([-0.75,count+0.5],[4.5,4.5],[8.5,8.5],facecolor='Pink')
scatter(D[:,0],D[:,1],s=D[:,2]*80,c=D[:,2],cmap='viridis_r')
c=colorbar(ticks=[1,2,3,4])
c.ax.set_ylabel('Count')
xticks(arange(0,count,1),vdata.keys(),rotation=90)
yticks(arange(0,len(order)+1,1),order)
title('lillie volunteers of 2020')
xlim([-0.75,count-0.25])
# text(28,7.75,'non-running roles',fontstyle='italic')


        