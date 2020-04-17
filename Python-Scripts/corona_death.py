#! /usr/bin/python3

import pandas as pd
import seaborn as sns



death=pd.read_csv('death.csv',encoding = "ISO-8859-1")
sns.catplot(x="Country",y="Deaths",kind='bar',data=death[:10],height=5).set_xticklabels(rotation=45).savefig('death.png')
