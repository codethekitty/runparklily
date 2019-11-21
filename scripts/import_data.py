from pylab import *
import pandas,glob,os
os.chdir(r'C:\Users\calvinwu\Google Drive\transfer folder\lillie')
#os.chdir('/Users/catbox/Google Drive/transfer folder/lillie')

#%% get all events

flist=glob.glob('event_data/event*')
flist=sort(flist)
headerlist=['pos','parkrunner','time','age_cat','age_grade','gender','gender_pos','club','note','total_runs','misc']

for enumber,ev in enumerate(flist):
    if enumber<52:
        data = pandas.read_csv(ev, header = None,sep='\t')
        data.columns=headerlist
    else:
        f=open(ev,'r').read()
        fl=f.split('\n')
        fll=[]
        for i in fl:
            fll.extend(i.split('\t'))
            
        fll=[x for x in fll if x]
        fll=[x for x in fll if x!=' ']
        
        i=1
        cont = sum(isin(fll,str(i+1)))
        data=[]
        while cont!=0:
            w1=where(isin(fll,str(i)))[0][0]
            w2=where(isin(fll,str(i+1)))[0][0]
            ff=fll[w1:w2]
            if ff[1]!='Unknown':
                time=[x for x in ff if (x.find(':')>0) and (x.find('PB')<0)][0]
                note=[x for x in ff if (x.find('First')>=0) or (x.find('PB')>=0)][0]
                agegrade=ff[6][:ff[6].find('%')]+' %'
                gp=int(ff[4][:ff[4].find('/')])
                add={'pos':int(ff[0]),'parkrunner':ff[1],'time':time,'age_cat':ff[5],'age_grade':agegrade,'gender':ff[3],'gender_pos':gp,'note':note,'total_runs':int(ff[2][:ff[2].find(' ')])}
            else:
                add={'pos':int(ff[0]),'parkrunner':ff[1],'time':nan,'age_cat':nan,'age_grade':nan,'gender':nan,'gender_pos':nan,'note':nan,'total_runs':nan}
            data.append(add)
            i+=1
            cont = sum(isin(fll,str(i+1)))
        w1=where(isin(fll,str(i)))[0][0]
        ff=fll[w1:]
        if ff[1]!='Unknown':
            time=[x for x in ff if (x.find(':')>0) and (x.find('PB')<0)][0]
            note=[x for x in ff if (x.find('First')>=0) or (x.find('PB')>=0)][0]
            agegrade=ff[6][:ff[6].find('%')]+' %'
            gp=int(ff[4][:ff[4].find('/')])
            add={'pos':int(ff[0]),'parkrunner':ff[1],'time':time,'age_cat':ff[5],'age_grade':agegrade,'gender':ff[3],'gender_pos':gp,'note':note,'total_runs':int(ff[2][:ff[2].find(' ')])}
        else:
            add={'pos':int(ff[0]),'parkrunner':ff[1],'time':nan,'age_cat':nan,'age_grade':nan,'gender':nan,'gender_pos':nan,'note':nan,'total_runs':nan}
        data.append(add)
        data=pandas.DataFrame.from_dict(data)


    data['event']=enumber+1
    if enumber==0:
        data_all=data
    else:
        data_all=pandas.concat([data_all,data],ignore_index=True,sort=True)
data_all = data_all.drop(columns=['misc','club'])
Dall=data_all.dropna()


