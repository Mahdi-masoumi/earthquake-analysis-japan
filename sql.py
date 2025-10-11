from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ARRAY, Date, Float, Text

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
