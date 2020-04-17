#! /usr/bin/python3

import pandas as pd
import seaborn as sns
import requests
import lxml.html as lh
import csv

source = requests.get("https://www.worldometers.info/coronavirus/")
doc = lh.fromstring(source.content)
tr_elements = doc.xpath('//tr')
India_map={}
i=0

def mk_int(s):
    return int(s) if s else 0

# Since out first row is the header, data is stored on the second row onwards
for j in range(1, len(tr_elements)):
    # T is our j'th row
    T = tr_elements[j]
    if(T[0].text_content() == 'India'):
        India_map[tr_elements[0][1].text_content()]=mk_int(tr_elements[j][1].text_content().replace(',',""))
        India_map[tr_elements[0][2].text_content()]=mk_int(tr_elements[j][2].text_content().replace(',',"").replace('+',""))
        India_map[tr_elements[0][3].text_content()]=mk_int(tr_elements[j][3].text_content().replace(',',""))
        India_map[tr_elements[0][4].text_content()]=mk_int(tr_elements[j][4].text_content().replace(',',"").replace('+',""))
        India_map['Recovered']=mk_int(tr_elements[j][5].text_content().replace(',',""))
        India_map[tr_elements[0][6].text_content()]=mk_int(tr_elements[j][6].text_content().replace(',',""))
        break


Category=list(India_map.keys())
Cases=list(India_map.values())

try:
    with open('india.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Category','Count'])
        for x,y in dict(zip(Category,Cases)).items():
            writer.writerow([x,y])
except IOError:
    print("I/O error")

india=pd.read_csv('india.csv',encoding = "ISO-8859-1")
sns.catplot(y="Count",x="Category",kind='bar',data=india).set_xticklabels(rotation=45).set_axis_labels(x_var='Corona In INDIA').savefig('india.png')
