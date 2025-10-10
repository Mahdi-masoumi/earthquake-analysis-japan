import requests
from bs4 import BeautifulSoup
url="https://geofon.gfz.de/eqinfo/list.php?datemin=2025-09-10&datemax=2025-10-10&latmax=46&lonmin=123&lonmax=146&latmin=24&magmin=1&fmt=html&nmax=1000"
response=requests.get(url)
if response.status_code==200:
    pass
else:
    print("ye chezish shode")
soup=BeautifulSoup(response.content,"html.parser")
