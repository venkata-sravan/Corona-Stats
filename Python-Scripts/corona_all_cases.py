#! /usr/bin/python3

import requests
import lxml.html as lh
import csv
import pandas as pd

source = requests.get("https://www.worldometers.info/coronavirus/")
doc = lh.fromstring(source.content)
tr_elements = doc.xpath('//tr')
Cases_Map={}
i=0
# Since out first row is the header, data is stored on the second row onwards
for j in range(1, int(len(tr_elements)/2)):
    # T is our j'th row
    z=['World','Total:','','Africa','Oceania','South America','Asia','Europe','North America','Country,Other','Asia']
    T = tr_elements[j]
    try:
        if (T[0].text_content().replace('\n', "").strip() not in z):
            Cases_Map[T[0].text_content()]=int(T[1].text_content().replace(',',""))
    except:
        pass

Cases_Map.pop('World',None)
Cases_Map.pop('Total:',None)
Cases_Map.pop('\n\n',None)
Cases_Map.pop('\nAfrica\n',None)
Cases_Map.pop('\nOceania\n',None)
Cases_Map.pop('\nSouth America\n',None)
Cases_Map.pop('\nAsia\n',None)
Cases_Map.pop('\nEurope\n',None)
Cases_Map.pop('\nNorth America\n',None)
Cases_Map=sorted(Cases_Map.items(), key = lambda x : x[1],reverse=True)
Cases_Map=dict(Cases_Map)
try:
    with open('cases.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Rank','Country', 'Cases'])
        i=0
        for key, value in Cases_Map.items():
            i=i+1
            writer.writerow([i,key, value])
except IOError:
    print("I/O error")

active=pd.read_csv('cases.csv',index_col=[0,1,2],encoding = "ISO-8859-1")
active.to_html('cases.html')
