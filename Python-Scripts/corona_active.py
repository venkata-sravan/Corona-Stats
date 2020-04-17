#! /usr/bin/python3

import pandas as pd
import seaborn as sns



active=pd.read_csv('active.csv',encoding = "ISO-8859-1")
sns.catplot(x="Country",y="Active Cases",kind='bar',data=active[:10],height=5).set_xticklabels(rotation=45).savefig('active.png')
