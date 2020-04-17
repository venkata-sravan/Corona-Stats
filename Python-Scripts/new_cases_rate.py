#! /usr/bin/python3

import requests
import lxml.html as lh
import csv
import pandas as pd
from math import ceil

source = requests.get("https://www.worldometers.info/coronavirus/")
doc = lh.fromstring(source.content)
tr_elements = doc.xpath('//tr')

def getMap(start,stop):
    New_Cases=[]
    New_Cases_Country=[]
    for j in range(start, stop):
        # T is our j'th row
        z=['Total:','','Africa','Oceania','South America','Asia','Europe','North America','Country,Other','Asia']
        T = tr_elements[j]
        try:
            if ((T[0].text_content().replace('\n', "").strip() not in z) and (int(T[2].text_content().replace(',', ""))!=0) and (int(T[1].text_content().replace(',', ""))>=1000)):
                New_Cases_Country.append(T[0].text_content())
                New_Cases.append(int(T[2].text_content().replace(',', "")))
        except:
            pass
    return New_Cases_Country,New_Cases
New_Cases_Country_Today,New_Cases_Today=getMap(1,int(len(tr_elements) / 2))
New_Cases_Country_Yesterday,New_Cases_Yesterday=getMap(int(len(tr_elements) / 2),len(tr_elements))
new_case_yesterday=dict(zip(New_Cases_Country_Yesterday,New_Cases_Yesterday))
new_case_today=dict(zip(New_Cases_Country_Today,New_Cases_Today))
new_case_final={}
for country in New_Cases_Country_Today:
    if (country in new_case_today.keys() and country in new_case_yesterday.keys()):
        new_case_final[country]=ceil((new_case_today[country]-new_case_yesterday[country])*100/new_case_yesterday[country])
new_case_final=sorted(new_case_final.items(), key = lambda x : x[1],reverse=True)
new_case_final=dict(new_case_final)
try:
    with open('new_case_rate.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Rank','Country', 'Daily Cases', 'Change in Cases'])
        i=0
        for key, value in new_case_final.items():
            i=i+1
            writer.writerow([i,key, new_case_today[key], str(value)+'%'])        
except IOError:
    print("I/O error")

new_cases=pd.read_csv('new_case_rate.csv',index_col=[0,1,2,3],encoding = "ISO-8859-1")
new_cases.to_html('change/daily_case_rate.html')

