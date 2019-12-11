from pylab import *
import requests
import time,datetime
from bs4 import BeautifulSoup
import re,os
#%% 

def scrape_this(url):
    cstr='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    
    headers = {'User-Agent': cstr}
    response = requests.get(url,headers=headers)
    if response.status_code==200:
        print('success')
    else:
        print('failed')
    return(response)
  
#%%
#df2 obtained from process1.py
    
urlhead='https://www.parkrun.us/results/athleteresultshistory/?athleteNumber='

dfc = df2.volunteer.value_counts()
dv = list(dfc[dfc>2].index)
df3 = df2[isin(df2.volunteer,dv)].drop(columns=['event','parkrun']).drop_duplicates()

for j,r in df3.iterrows():
    url = urlhead+r.barcode
    response = scrape_this(url)
    soup=BeautifulSoup(response.text,'html.parser')
    section = soup.find_all('h1')[2].parent
    items = [x.find_all('td') for x in section.find_all('tr')]
    vdata=[]
    for i in items:
        if len(i)>0:
            vdata.append([x.text for x in i])
    V={'barcode':r.barcode,'volunteer':r.volunteer,'data':vdata,'last_updated':datetime.datetime.now()}
    save(os.path.join('shared\\data\\raw_data\\volunteer_data','a'+r.barcode+'.npy'),V)
    print(j,len(df3),r.volunteer)
    time.sleep(random(1)[0]*5+2)
    
#%%