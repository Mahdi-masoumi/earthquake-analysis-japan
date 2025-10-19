from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date, text
import pandas as pd
# nima part
files = [
    ("/Users/Vengeance/Documents/GitHub/earthquake-analysis-japan/JAPAN_DATASET_cleaned.csv", "Dataset"),
    ("/Users/Vengeance/Documents/GitHub/earthquake-analysis-japan/JAPAN_EMSC_cleaned.csv", "EMSC"),
    ("/Users/Vengeance/Documents/GitHub/earthquake-analysis-japan/JAPAN_GEOFON_cleaned.csv", "GEOFON"),
    ("/Users/Vengeance/Documents/GitHub/earthquake-analysis-japan/JAPAN_USGS_cleaned.csv", "USGS")
]

dfs = []

for file_path, source_name in files:
    df = pd.read_csv(file_path)
    if 'place' in df.columns and 'region' in df.columns:
        df = df.drop(columns=['place'])
    if 'latitude' in df.columns and 'longitude' in df.columns:
        df['coordination'] = df.apply(
            lambda x: f"[{x.latitude}, {x.longitude}]", axis=1)
    rename_map = {}
    if 'mag' in df.columns:
        rename_map['mag'] = 'magnitude'
    if 'place' in df.columns and 'region' not in df.columns:
        rename_map['place'] = 'region'
    df = df.rename(columns=rename_map)
    df['source'] = source_name
    columns_needed = ['time', 'coordination',
                      'depth', 'magnitude', 'region', 'source']
    df = df[[c for c in columns_needed if c in df.columns]]
    if 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'], errors='coerce').dt.date
    if 'depth' in df.columns:
        df['depth'] = pd.to_numeric(df['depth'], errors='coerce')
    if 'magnitude' in df.columns:
        df['magnitude'] = pd.to_numeric(df['magnitude'], errors='coerce')
    dfs.append(df)

df_all = pd.concat(dfs, ignore_index=True)
df_all = df_all.dropna(subset=['time', 'magnitude', 'region'])
df_all = df_all.drop_duplicates()

engine = create_engine(
    "mysql+pymysql://root:nimaaslrousta717@localhost:3306/earthquakes_db")
connection = engine.connect()
metadata = MetaData()

earthquakes = Table(
    'Earthquakes',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('time', Date),
    Column('coordination', String(50)),
    Column('depth', Float),
    Column('magnitude', Float),
    Column('region', String(100)),
    Column('source', String(50))
)

connection.execute(text("DROP TABLE IF EXISTS Earthquakes;"))
metadata.create_all(engine)

df_all.to_sql(
    name='Earthquakes',
    con=engine,
    if_exists='append',
    index=False,
    chunksize=1000
)

count = connection.execute(text("SELECT COUNT(*) FROM Earthquakes;")).scalar()
print(f"Number of rows inserted: {count}")
# sepehr queries
queries = {
    "total_earthquakes": """
        SELECT region, EXTRACT(MONTH FROM time) AS month, COUNT(*) AS total_earthquakes
        FROM Earthquakes
        GROUP BY region, month;
    """,
    "avg_magnitude": """
        SELECT region, source, AVG(magnitude) AS avg_magnitude
        FROM Earthquakes
        GROUP BY region, source;
    """,
    "top_earthquakes": """
        SELECT *
        FROM Earthquakes
        ORDER BY magnitude DESC, time DESC
        LIMIT 10;
    """,
    "depth_range": """
        SELECT region, MAX(depth) AS max_depth, MIN(depth) AS min_depth
        FROM Earthquakes
        GROUP BY region;
    """,
    "delete_invalid": """
        DELETE FROM Earthquakes
        WHERE magnitude < 0
           OR magnitude > 10
           OR depth < 0;
    """,
    "update_null_magnitude": """
        UPDATE Earthquakes
        SET magnitude = 0
        WHERE magnitude IS NULL;
    """,
    "update_null_depth": """
        UPDATE Earthquakes
        SET depth = 0
        WHERE depth IS NULL;
    """
}

for q in queries.values():
    connection.execute(text(q))

result = connection.execute(
    text("SELECT id, time, coordination, depth, magnitude, region, source FROM Earthquakes LIMIT 5;")
).fetchall()
for row in result:
    print(row)

output_path = "Earthquakes_export.csv"
df_export = pd.read_sql("SELECT * FROM Earthquakes", con=engine)
df_export.to_csv(output_path, index=False, encoding='utf-8-sig')
