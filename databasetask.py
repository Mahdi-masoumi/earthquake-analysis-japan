from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date, text
import pandas as pd
from dotenv import load_dotenv
import os

def run_database_final_debug():
    load_dotenv()
    password = os.getenv("DB_PASSWORD")
    engine = create_engine(f"mysql+pymysql://root:nimaaslrousta717@localhost:3306/earthquakes_db")
    connection = engine.connect()
    metadata = MetaData()

    files = [
        ("JAPAN_DATASET_cleaned.csv", "Dataset"),
        ("JAPAN_EMSC_cleaned.csv", "EMSC"),
        ("JAPAN_GEOFON_cleaned.csv", "GEOFON"),
        ("JAPAN_USGS_cleaned.csv", "USGS")
    ]

    def clean_df(df, source_name):
        if 'place' in df.columns and 'region' in df.columns:
            df = df.drop(columns=['place'])
        if 'latitude' in df.columns and 'longitude' in df.columns:
<<<<<<< HEAD
            df['coordination'] = df.apply(lambda x: f"[{x.latitude}, {x.longitude}]", axis=1)
=======
            df['coordination'] = df.apply(
                lambda x: f"[{x.latitude}, {x.longitude}]", axis=1)
        else:
            df['coordination'] = None

>>>>>>> 462185258217c62b7f315bd4c76cab7aa3036316
        rename_map = {}
        if 'mag' in df.columns:
            rename_map['mag'] = 'magnitude'
        if 'place' in df.columns and 'region' not in df.columns:
            rename_map['place'] = 'region'
        df = df.rename(columns=rename_map)
        df['source'] = source_name
        if 'time' in df.columns:
            df['time'] = pd.to_datetime(df['time'], errors='coerce').dt.date
<<<<<<< HEAD
        if 'depth' in df.columns:
            df['depth'] = pd.to_numeric(df['depth'], errors='coerce')
        if 'magnitude' in df.columns:
            df['magnitude'] = pd.to_numeric(df['magnitude'], errors='coerce')
=======
        else:
            df['time'] = None

        df['depth'] = pd.to_numeric(df.get('depth'), errors='coerce')
        df['magnitude'] = pd.to_numeric(df.get('magnitude'), errors='coerce')
        df['source'] = source_name

        keep_cols = ['time', 'coordination',
                     'depth', 'magnitude', 'region', 'source']
        df = df[keep_cols]

>>>>>>> 462185258217c62b7f315bd4c76cab7aa3036316
        return df

    for file_path, source_name in files:
        df = pd.read_csv(file_path)
        df = clean_df(df, source_name)
        table_name = f"Earthquakes_{source_name}"
        connection.execute(text(f"DROP TABLE IF EXISTS {table_name};"))
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False, chunksize=1000)

        count = connection.execute(text(f"SELECT COUNT(*) FROM {table_name};")).scalar()
        print(f"Inserted into {table_name}: {count} rows")

    connection.execute(text("DROP TABLE IF EXISTS Earthquakes;"))
    earthquakes = Table(
        'Earthquakes', metadata,
        Column('id', Integer, primary_key=True),
        Column('time', Date),
        Column('coordination', String(50)),
        Column('depth', Float),
        Column('magnitude', Float),
        Column('region', String(100)),
        Column('source', String(50))
    )
    metadata.create_all(engine)

    insert_query = text("""
        INSERT INTO Earthquakes (time, coordination, depth, magnitude, region, source)
        SELECT time, coordination, depth, magnitude, region, source
        FROM (
            SELECT time, coordination, depth, magnitude, region, source FROM Earthquakes_Dataset
            UNION ALL
            SELECT time, coordination, depth, magnitude, region, source FROM Earthquakes_EMSC
            UNION ALL
            SELECT time, coordination, depth, magnitude, region, source FROM Earthquakes_GEOFON
            UNION ALL
            SELECT time, coordination, depth, magnitude, region, source FROM Earthquakes_USGS
        ) AS combined
        WHERE time IS NOT NULL AND magnitude IS NOT NULL AND region IS NOT NULL;
    """)

    with engine.begin() as conn:
        conn.execute(insert_query)

    final_count = connection.execute(text("SELECT COUNT(*) FROM Earthquakes;")).scalar()
    print(f"FINAL TABLE COUNT: {final_count}")

    if final_count == 0:
        debug_union = connection.execute(text("""
            SELECT COUNT(*) FROM (
                SELECT time, coordination, depth, magnitude, region, source FROM Earthquakes_Dataset
                UNION ALL
                SELECT time, coordination, depth, magnitude, region, source FROM Earthquakes_EMSC
                UNION ALL
                SELECT time, coordination, depth, magnitude, region, source FROM Earthquakes_GEOFON
                UNION ALL
                SELECT time, coordination, depth, magnitude, region, source FROM Earthquakes_USGS
            ) AS combined;
        """)).scalar()
        print(f"UNION ALL total rows before filter: {debug_union}")

        debug_non_null = connection.execute(text("""
            SELECT COUNT(*) FROM (
                SELECT time, coordination, depth, magnitude, region, source FROM Earthquakes_Dataset
                UNION ALL
                SELECT time, coordination, depth, magnitude, region, source FROM Earthquakes_EMSC
                UNION ALL
                SELECT time, coordination, depth, magnitude, region, source FROM Earthquakes_GEOFON
                UNION ALL
                SELECT time, coordination, depth, magnitude, region, source FROM Earthquakes_USGS
            ) AS combined
            WHERE time IS NOT NULL AND magnitude IS NOT NULL AND region IS NOT NULL;
        """)).scalar()
        print(f"Rows surviving after WHERE filter: {debug_non_null}")

run_database_final_debug()