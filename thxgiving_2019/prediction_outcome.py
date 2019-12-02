from pylab import *
import pandas

#%%
f=open('thxgiving_2019/prediction_result.txt')
data=f.read().split('\n')[:-1]
result=[]
for i in arange(0,len(data)-2,3):
    result.append([data[i],data[i+1],data[i+2]])
R=pandas.DataFrame.from_records(result,columns=['parkrun','prediction','actual'])
X=R.index.values
Y1=array([int(x) for x in R.prediction.values])
Y2=array([int(x) for x in R.actual.values])
plot(X,Y1,'x',label='prediction')
plot(X,Y2,'.-',label='actual')
xticks(X,R.parkrun,rotation=45,ha='right')
ylabel('Attendance')
legend()
title('total actual (predicted): %d (%d)'%(sum(Y2),sum(Y1)))
savefig('../outcome.png',dpi=150,bbox_inches='tight')
