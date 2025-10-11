from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ARRAY, Date, Float, Text
import pandas as pd



df = pd.read_csv("/Users/Vengeance/Documents/GitHub/earthquake-analysis-japan/JAPAN_DATASET.csv")
df.head()







engine = create_engine('sqlite:///mydb.db')
connection = engine.connect()
metadata = MetaData()

earthquakes = Table('Earthquakes',
                    metadata,
                    Column('id', Integer, primary_key=True),
                    Column('time', Date)#not sure yet
                    Column('coordination', ARRAY)#not sure yet
                    Column('depth', Float)
                    Column('magnitude', Float)
                    Column('region',String)
                    Column('source', String)
                    )   
def insert_data(time, coordination, depth, magnitude, region, source):
    earthquakes.insert().values(time= time, coordination= coordination, depth= depth, magnitude= magnitude, region= region, source= source)
