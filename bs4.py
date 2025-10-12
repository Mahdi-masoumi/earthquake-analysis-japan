import requests
from bs4 import BeautifulSoup
import pandas as pd 
url="https://geofon.gfz.de/eqinfo/list.php?datemin=2025-09-10&datemax=2025-10-10&latmax=46&lonmin=123&lonmax=146&latmin=24&magmin=1&fmt=html&nmax=1000"
response=requests.get(url)
if response.status_code==200:
    pass
else:
    print("ye chezish shode")
soup=BeautifulSoup(response.content,"html.parser")
earthquake=[]
for a in soup.find_all("a",href=True):
    earthquake.append(a)
for earth in earthquake :
    mag=earth.find("span",class_="magbox").text
    place=earth.find("strong").text
    time=earth.find("div",class_="col-xs-12")[1].text
    depth=earth.find_all("span",class_="pull-right")[0].text.replace("*","")
data=[]
for dataa in earthquake:
    a= {
        'time': time,
        'depth': depth,
        'mag': mag,
        'place': place
    }
    data.append(a)
df=pd.DataFrame(data)
df.to_csv("eathquakes.csv")
print(data)
    

    
