from pylab import *
import pandas,os,re
import time,datetime


#%%
folder_list = os.listdir('raw_data')
P=[]
V=[]
for f in folder_list:
    for ev in os.listdir(os.path.join('raw_data',f)):
        ev_number = int(ev[5:-4])
        L=load(os.path.join('raw_data',f,ev),allow_pickle=True).item()
        
        for v in L['volunteers']:
            V.append({'volunteer':v[0],'barcode':v[1],'parkrun':f,'event':ev_number})
        positions = [x for x in L if type(x)==int]
        for p in positions:
            if L[p][0]!='Unknown':
                pdata = [re.sub(' +',' ',x.strip()) for x in '|'.join(L[p]).split('|')]
                soup = ''.join(pdata[2:])
                if (soup.find('Female')>=0) & (soup.find('Male')==-1):
                    g='W'
                else:
                    g='M'
                soup = [x for x in pdata[2:] if len(x)>1]
                agecat = [x for x in soup if x[1]==g]
                if len(agecat)==0:
                    agecat=['Unknown']
                agegrade = [x for x in soup if x.find('age grade')>=0]
                if len(agegrade)>0:
                    agegrade=agegrade[0]
                    agegrade=agegrade[:agegrade.find('%')]
                else:
                    agegrade=nan
                finishtime=[x for x in soup if (x.find(':')>=0)&(x.find('PB')<0)&(x.find('http')<0)][0]
                P.append({'parkrun':f,'event':ev_number,'position':p,'parkrunner':pdata[0],'nprs':pdata[1],'time':finishtime,'age_cat':agecat[0],'age_grade':float(agegrade)})
    print(f)
df=pandas.DataFrame.from_dict(P)
df2=pandas.DataFrame.from_dict(V)    
#%%
fn = datetime.datetime.now().strftime('%Y_%m_%d')
df.to_csv('shared/run_data_'+fn+'.csv',index=False)
df2.to_csv('shared/volunteer_data_'+fn+'.csv',index=False)

#%%
