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

data = [{
    'time': eq.findChildren()[6].text.split()[:2][0] + " " + eq.findChildren()[6].text.split()[:2][1],
    'depth': eq.find_all("span", class_="pull-right")[0].text.strip().replace("*", ""),
    'mag': eq.find(class_="magbox").text.strip(),
    'place': eq.find("strong").text.strip()
} for eq in earthquakes]

df = pd.DataFrame(data)
df.to_csv("scraping/JAPAN_GEOFON.csv")
# print(data)
