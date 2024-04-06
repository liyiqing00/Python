from xml.etree.ElementTree import *
import urllib.request
import cgi
import sys,io
import csv
import requests
import json
from dataclasses import dataclass

filepath1='tour.csv'
filepath2='code.csv'
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
form=cgi.FieldStorage()
city=form.getvalue('city','')
genre=form.getlist('genre')


with open(filepath1, encoding="utf-8") as f:
    reader = csv.reader(f)
    tour = [r for r in reader]
    
with open(filepath2, encoding="utf-8") as f:
    reader = csv.reader(f)
    codes = [r for r in reader]

tree=fromstring(urllib.request.urlopen(
    urllib.request.Request(
        'http://weather.livedoor.com/forecast/rss/primary_area.xml')).read())

def search_node(node,city):
    if node.tag=='city':
        if node.attrib['title']==city:
            return node.attrib['id']
    for child in node:
        result=search_node(child,city)
        if result is not None:
            return result
    return None

cityid=search_node(tree,city)

response=requests.get(
    'http://weather.livedoor.com/forecast/webservice/json/v1',
    params={'city':cityid})

@dataclass
class Temp:
    date: str=""
    image: dict=None
    tempMax:str=""
    tempMin:str=""

result=json.loads(response.text)
loc=result['location']['city']
pref=result['location']['prefecture']

show_dates=[]
def temp_date(n):
    show_date=Temp()
    show_date.date = result['forecasts'][n]['dateLabel']
    show_date.image = result['forecasts'][n]['image']
    if result['forecasts'][n]['temperature']['max']:
       show_date.tempMax = result['forecasts'][n]['temperature']['max']['celsius']
    else:
        show_date.tempMax = ""
    if result['forecasts'][n]['temperature']['min']:
        show_date.tempMin = result['forecasts'][n]['temperature']['min']['celsius']
    else:
        show_date.tempMin = ""
    return show_date

for a in range(2):
    show_dates.append(temp_date(a))

for code in codes:
    if pref==code[1]:
        pref_code=code[0]

name=[]
def search_arrival(code):
    for t in tour:
        if code==t[1]:
            if t[0] not in name:
                name.append(t[0])

search_arrival(pref_code)

found=[]
if genre==[]:
    found=name
else:
    for t in tour:
        for g in genre:
            if g==t[3] and t[0] in name:
                if t[0] not in found:
                    found.append(t[0])

contents=""
for show_date in show_dates:
    contents+=f"<h1 align='center'><font size='4' color='#669999'>{show_date.date}の天気</font></h1>"
    contents+=f"<p align='center'><img width = {show_date.image['width']} heigth = {show_date.image['height']} src = {show_date.image['url']} title = {show_date.image['title']}></p>"
    contents+=f"<p align='center'>最高気温: {show_date.tempMax}(度)</p>"
    contents+=f"<p align='center'>最低気温: {show_date.tempMin}(度)</p>"
contents+="<fieldset><div style='background-color:#CCFFFF'>"
contents+=f"<legend align='center'><font size='4'>{pref}にある"
if genre==[]:
    contents+="旅行資源</font></legend>"
else:
    for g in genre:
        contents += f"「{g}」　"
contents+="</font></legend>"

if found==[]:
    contents+="<p align='center'>見つかりませんでした</p>"
else:
    contents+="<div style='display:flex;flex-wrap:wrap;color:#778899'>"
    for n in found:
        contents+=f"<div style=' width:calc(100%/3)'><li>{n}</li></div>"
    contents+="</div>"
    contents+="</div>"
    contents+="</fieldset>"



template="""
<!DOCTYPE>
<html>
<head>
    <meta charset="utf-8">
    <title>Find</title>
</head>
<body>
    <form method="POST" action="find.py">
    <fieldset>
    <legend align="center"><font size="4">{city}</font></legend>
    </fieldset>
    {contents}
</body>
</html>
"""

result=template.format(city=city,width="width:calc(100%/3);",contents=contents)
print("Content-type: text/html\n")
print(result)
