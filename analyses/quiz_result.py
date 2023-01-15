from pylab import *
import pandas,glob
pandas.set_option('display.max_columns',None)

#%%
file = 'data/quiz_result_200418.csv'
df = pandas.read_csv(file)

answers=list(df.iloc[-1,3:])
for i in range(3,len(list(df))):    
    df.iloc[:,i]=(df.iloc[:,i]==answers[i-3])*1

tbl = df.iloc[:-1,3:].values

figure(figsize=(8,5))
pcolormesh(tbl,cmap='binary')

y1=[x[:x.find('/')-1] for x in df.iloc[:,1]]
y2=df.iloc[:,2]
ytag=y2+' ('+y1+')'

yticks(arange(shape(tbl)[0])+0.5,ytag)
xticks(arange(shape(tbl)[1])+0.5,['Q'+str(x+1) for x in arange(shape(tbl)[1])])

savefig('temp.png',dpi=300,bbox_inches='tight')

#%%
F=glob.glob('data/quiz_result*')
rc=rcParams['axes.prop_cycle'].by_key()['color']
c=0
figure(figsize=(8,4))
D=[]
for f in sort(F):
    date=f[f.find('_result_')+8:f.find('.csv')]
    date='Quiz #'+str(c+1)+' ('+date[3:4]+'/'+date[4:]+')'
    D.append(date)
    df = pandas.read_csv(f)
    if 'Score' not in list(df):
        ix=[x for x in list(df) if 'core' in x][0]
        t=[int(x[:x.find('.')]) for x in df[ix]]
    else:
        ix='Score'
        t=[int(x[:x.find('/')-1]) for x in df[ix]]
    maxscore=int(df[ix][0][df[ix][0].find('/')+1:])
    t=array(t)[~isin(t,maxscore)]
    h=histogram(t,arange(0,maxscore+1))[0]
    for i in arange(1,max(h)+1):
        ts=where(h>=i)[0]
        plot(ts/maxscore,[c]*len(ts)+(i-1)/8,'o',color=rc[c],ms=4)
    plot(unique(t)/maxscore,[c]*len(unique(t)),'o',color=rc[c],ms=4)
    errorbar(mean(t/maxscore),c-0.2,0,std(t/maxscore),color=rc[c])
    plot(mean(t/maxscore),c-0.2,'^',ms=8,color=rc[c])
    c+=1
xlim(0,1)
xticks(arange(0,1.2,0.2),[int(x) for x in arange(0,1.2,0.2)*100])
xlabel('% Score')
yticks(arange(5),D)
savefig('temp3.png',dpi=300,bbox_inches='tight')

    
    
