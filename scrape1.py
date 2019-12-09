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
        

#%% get list of US parkrun by scraping a single page
url = 'https://www.parkrun.us/special-events/'
response = scrape_this(url)
soup=BeautifulSoup(response.text,'html.parser')
all_prs = soup.find_all('a',href=re.compile('parkrun'),text=re.compile('parkrun'))[1:]
parkruns={}
for s in all_prs:
    parkruns[s.text]=s.get('href')

#%%
for K,V in parkruns.items():
    if K[:3]>='Liv':
        Kpath = os.path.join('raw_data',K)
        if not(os.path.exists(Kpath)):
            os.mkdir(Kpath)
        url = V+'results/eventhistory'
        response = scrape_this(url)
        time.sleep(random(1)[0]*5+4)
        assert response.status_code==200
        print(K)
        soup=BeautifulSoup(response.text,'html.parser')
        allevents = soup.find_all('a',href=re.compile('runSeqNumber'),text=re.compile('/'))
        for s in allevents:
            eventdate = s.text
            eventurl = V+'results'+s.get('href')[2:]
            eventnumber=int(eventurl[eventurl.find('SeqNumber')+10:])
            fn='event'+str(eventnumber)+'.npy'
            if not(os.path.exists(os.path.join(Kpath,fn))):
                response = scrape_this(eventurl)
                assert response.status_code==200
                soup=BeautifulSoup(response.text,'html.parser')
                volunteer = soup.find_all('p')[4].find_all('a')
                vlist=[]
                for vol in volunteer:
                    vlist.append([vol.text,vol.get('href')[vol.get('href').find('=')+1:]])
                tbl = soup.find('table')
                result={}
                result['parkrun']=K
                result['event_date']=eventdate
                result['event_number']=eventnumber
                result['volunteers']=vlist
                result['last_updated']=datetime.datetime.now()
                for n,r in enumerate(tbl.find_all('tr')[1:]):
                #    ele = r.find_all('div',{'class':'detailed'})
                    textadd=[]
                    ele = r.find_all('td')
                    for i in ele:
                        j=i.find_all('div')
                        for k in j:
                            textadd.append(k.text.replace('\n','').replace('\xa0','').replace('  ',' ').rstrip().lstrip())
                    result[n+1]=textadd
                save(os.path.join(Kpath,fn),result)
                print(K,eventnumber)
                t=random(1)*3+3
                time.sleep(t[0])
                
