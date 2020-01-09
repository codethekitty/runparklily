#%% most tourism
thisparkrun = df[df.parkrun.str.find('Lillie')>=0]
otherparkrun = df[df.parkrun.str.find('Lillie')<0]
parkrunner_list = thisparkrun.parkrunner.value_counts()
parkrunner_list = parkrunner_list[parkrunner_list>5]

tourist=[]
for p,i in parkrunner_list.items():
    check = sum(otherparkrun.parkrunner==p)>0
    if bool(check):
        n_other = len(otherparkrun[otherparkrun.parkrunner==p].parkrun.unique())
        l_other = otherparkrun[otherparkrun.parkrunner==p].parkrun.unique()
        d={'runner':p,'count':n_other,'list':l_other}
        tourist.append(d)
        print(p,n_other)


   