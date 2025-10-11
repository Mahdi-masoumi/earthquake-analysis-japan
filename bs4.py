import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://geofon.gfz.de/eqinfo/list.php?datemin=2025-09-10&datemax=2025-10-10&latmax=46&lonmin=123&lonmax=146&latmin=24&magmin=1&fmt=html&nmax=1000"
response = requests.get(url)
if response.status_code == 200:
    pass
else:
    print("ye chezish shode")

soup = BeautifulSoup(response.content, "html.parser")
earthquakes = []
for div in soup.select(".flex-row.row.eqinfo-all"):
    earthquakes.append(div)

data = []
for eq in earthquakes:
    parent= eq.find_all("div", class_="col-xs-12")[1]
    depth_ = parent.find("span", class_="pull-right")
    depth = ""
    if depth_:
        depth__ = depth_.get_text(strip=True)
        depth = depth__.replace("*", "").replace("\xa0","")
    data.append({
        'time': parent.contents[0],
        'depth': depth,
        'mag': eq.find(class_="magbox").text,
        'place': eq.find("strong").text
    })

df = pd.DataFrame(data)
df.to_csv("earthquakesz.csv")