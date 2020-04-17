#! /usr/bin/python3
import pandas as pd
import seaborn as sns



cases=pd.read_csv('cases.csv',encoding = "ISO-8859-1")
sns.catplot(x="Country",y="Cases",kind='bar',data=cases[:10],height=5).set_xticklabels(rotation=45).savefig('cases.png')
