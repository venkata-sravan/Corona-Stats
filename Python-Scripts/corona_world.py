#! /usr/bin/python3

import pandas as pd
import seaborn as sns
import csv
import requests
import lxml.html as lh

source = requests.get("https://www.worldometers.info/coronavirus/")
doc = lh.fromstring(source.content)
tr_elements = doc.xpath('//tr')
World_map={}
i=0
# Since out first row is the header, data is stored on the second row onwards
for j in range(1, len(tr_elements)):
    # T is our j'th row
    T = tr_elements[j]
    if(T[0].text_content() == 'World'):
        World_map[tr_elements[0][1].text_content()]=int(tr_elements[j][1].text_content().replace(',',""))
        World_map[tr_elements[0][2].text_content()]=int(tr_elements[j][2].text_content().replace(',',"").replace('+',""))
        World_map[tr_elements[0][3].text_content()]=int(tr_elements[j][3].text_content().replace(',',""))
        World_map[tr_elements[0][4].text_content()]=int(tr_elements[j][4].text_content().replace(',',"").replace('+',""))
        World_map['Recovered']=int(tr_elements[j][5].text_content().replace(',',""))
        World_map[tr_elements[0][6].text_content()]=int(tr_elements[j][6].text_content().replace(',',""))
        break

Category=list(World_map.keys())
Cases=list(World_map.values())

try:
    with open('world.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Category','Count'])
        for x,y in dict(zip(Category,Cases)).items():
            writer.writerow([x,y])
except IOError:
    print("I/O error")

india=pd.read_csv('world.csv',encoding = "ISO-8859-1")
sns.catplot(y="Count",x="Category",kind='bar',data=india).set_xticklabels(rotation=45).set_axis_labels(x_var='Corona In WORLD',y_var='Cases in Million').savefig('world.png')
