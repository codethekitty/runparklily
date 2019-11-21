from pylab import *
import pandas
#%% from top500, no longer exist after main database is saved.

#f=open('parkrunner_number.txt','r').read()
#fa = f.find('athleteNumber=')
#data=[]
#while fa!=-1:
#    fi=f[fa+14:fa+90]
#    prnumber = int(fi[:fi.find('\">')])
#    prname = fi[fi.find('\">')+2:fi.find('</a>')]
##    print(prnumber,prname)
#    data.append({'parkrunner':prname,'a_number':prnumber})
#    f=f[fa+90:]
#    fa = f.find('athleteNumber=')
#df1=pandas.DataFrame.from_dict(data)

#%% read main database

df1=pandas.read_csv('parkrunner_number.csv')

#%% from weekly result, update main database

f=open('parkrunner_number_update.txt','r').read()
f=f[:f.find('Thanks to the volunteers')]
fa = f.find('athleteNumber=')
data=[]
while fa!=-1:
    fi=f[fa+14:fa+90]
    prnumber = int(fi[:fi.find('\" target')])
    prname = fi[fi.find('\">')+2:fi.find('</a>')]
    data.append({'parkrunner':prname,'a_number':prnumber})
    f=f[fa+90:]
    fa = f.find('athleteNumber=')
    
df2=pandas.DataFrame.from_dict(data)
df = pandas.concat([df1,df2]).drop_duplicates()
nft = len(df)-len(df1)
df.to_csv('parkrunner_number.csv',index=False)
print('%s first timer added to database.'%(nft))