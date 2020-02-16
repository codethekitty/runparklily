from matplotlib import gridspec
import matplotlib.patches as patches

#%%
gs=gridspec.GridSpec(7,6)

prs = df.parkrun.unique()
b=hstack((array([9.5,10.5,14.5,17.5,19.5]),arange(24.5,94.5,5),105))
blab=[10,12.5,16,18.5,22,27,32,37,42,47,52,57,62,67,72,77,82,87,90]
blab2=unique([x[2:] for x in df.age_cat.unique() if (x[-1]=='0')|(x[-1]=='4')|(x[-1]=='9')|(x[-1]=='7')])
blab2=hstack(('J10',blab2[2:],'90+'))

rcParams.update({'font.size': 12})

figure(figsize=(16,18))
for i,pr in enumerate(prs):
    ac = df.iloc[df[df.parkrun==pr].loc[:,'parkrunner'].drop_duplicates().index,-2]
    ac=ac[(ac!='Unknown')&(ac.str.find('--')==-1)]
    gender = [x[1] for x in ac]
    age = [int(x[2:4]) for x in ac]
    sub1=subplot(gs[i])
    # print(pr,mean(age))
    for s,sign,color in zip(('M','W'),(1,-1),('#0165fc','#ff81c0')):
        a=array(age)[isin(gender,s)]
        h=histogram(a,b)[0] #/len(gender)
        plot(h*sign,blab,'-',c=color,ms=14)
        x,y=(max(h),blab[argmax(h)])
        if sign==1:
            al='left'
        else:
            al='right'
        if s==ac.value_counts().index[0][1]:
            plot(x*sign,y,'o',c=color)
        p=round(sum(isin(gender,s))/len(gender)*100)
        text(max(h)*sign/3*2,75,str(int(p))+'%'+s,c=color,ha=al)
    title(pr[:pr.find('parkrun')-1],fontsize=13)
    ax=gca()
    xl=array(gca().get_xlim())
    xlim(max(abs(xl))*-1,max(abs(xl)))
    xticks(ax.get_xticks(),[int(x) for x in abs(ax.get_xticks())])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    yticks([])
    yt=[10,30,50,70]
    xl=gca().get_xlim()
    ylim(5,90)
    for y in yt:
        plot(xl,[y,y],'k:')
        text(min(xl),y,str(y),ha='right')
    yl=gca().get_ylim()
    plot((0,0),yl,'k-',lw=0.8)
tight_layout()
savefig('t5.png',dpi=300,bbox_inches='tight')

#%%
# Acorss all US parkruns, M45-49 is the most populous age category, followed by W40-44.
# Livonia is overrun (pun unintended) by kids: JM10 and JW10 are the largest age categories
# McAllister has the lowest proportion of U18 parkrunners: 6.4% compared to 26.5% of Livonia (Lillie: 17%)
# James Wilson from College Park retains the record of the oldest parkrunner: VM100-104
# Charleston, WV has the most unequal gender ratio with almost 60% female
# Crissy Field is the most-visited parkrun: 9666 (Lillie: 766). Thanks, Karl*

#%%
for i,pr in enumerate(prs):
    df1=df[df.parkrun==pr]
    if max(df1.event)<69:
        print(pr,max(df1.event+1))