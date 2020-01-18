from matplotlib import gridspec
#%
parkrunlist = list(df.parkrun.unique())
result=[]
for p in parkrunlist:
    leaders = df[df.parkrun==p].parkrunner.value_counts()
    leaders=leaders[leaders>max(leaders)/10]
    leaders=leaders.index
    print(len(leaders),df[df.parkrun==p].event.max())
    most_conseq_parkrun=[]
    for leader in leaders:
        a=sort(df[(df.parkrun==p) & (df.parkrunner==leader)].event.values)
        if all(diff(a)>0):
            count=1
            last_value=a[0]
            countS=[]
            for i in a[1:]:
                if i==last_value+1:
                    count+=1
                else:
                    countS.append(count)
                    count=1
                last_value=i
            if len(countS)>0:
                most_conseq=max(countS)
            else:
                most_conseq=len(a)
            conseq_loc=[]
            for i in range(len(a)):
                if len(a[i:i+most_conseq])==most_conseq:
                    if std(diff(a[i:i+most_conseq]))==0:
                        conseq_loc=a[i:i+most_conseq]
            cur=df[df.parkrun==p].event.max()
            # most_conseq_parkrun.append(most_conseq)
        # if most_conseq>=max(most_conseq_parkrun):
            if most_conseq>2:
                result.append({'parkrun':p,'leader':leader,'most_conseq':most_conseq,'events':conseq_loc,'current':cur})
                print(p,leader,most_conseq)
                    

scott=pandas.DataFrame.from_dict(result)




