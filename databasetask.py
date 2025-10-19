from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date, text
import pandas as pd
from dotenv import load_dotenv
import os


def run_database_final():
    load_dotenv()
    password = os.getenv("DB_PASSWORD")
    engine = create_engine(
        f"mysql+pymysql://root:{password}@localhost:3306/earthquakes_db")
    connection = engine.connect()
    metadata = MetaData()

    # nima part
    files = [
        ("JAPAN_DATASET_cleaned.csv", "Dataset"),
        ("JAPAN_EMSC_cleaned.csv", "EMSC"),
        ("JAPAN_GEOFON_cleaned.csv", "GEOFON"),
        ("JAPAN_USGS_cleaned.csv", "USGS")
    ]

    def clean_df(df, source_name):
        if 'Unnamed: 0' in df.columns:
            df = df.drop(columns=['Unnamed: 0'])

        if 'latitude' in df.columns and 'longitude' in df.columns:
            df['coordination'] = df.apply(
                lambda x: f"[{x.latitude}, {x.longitude}]", axis=1)
        else:
            df['coordination'] = None

        rename_map = {}
        if 'mag' in df.columns:
            rename_map['mag'] = 'magnitude'
        elif 'Magnitude' in df.columns:
            rename_map['Magnitude'] = 'magnitude'

        if 'place' in df.columns and 'region' not in df.columns:
            rename_map['place'] = 'region'
        elif 'region' not in df.columns:
            df['region'] = None

        df = df.rename(columns=rename_map)

        if 'time' in df.columns:
            df['time'] = pd.to_datetime(df['time'], errors='coerce').dt.date
        else:
            df['time'] = None

        df['depth'] = pd.to_numeric(df.get('depth'), errors='coerce')
        df['magnitude'] = pd.to_numeric(df.get('magnitude'), errors='coerce')
        df['source'] = source_name

        keep_cols = ['time', 'coordination',
                     'depth', 'magnitude', 'region', 'source']
        df = df[keep_cols]

        return df

    for file_path, source_name in files:
        df = pd.read_csv(file_path)
        df = clean_df(df, source_name)
        table_name = f"Earthquakes_{source_name}"
        connection.execute(text(f"DROP TABLE IF EXISTS {table_name};"))
        df.to_sql(name=table_name, con=engine,
                  if_exists='replace', index=False, chunksize=1000)

    connection.execute(text("DROP TABLE IF EXISTS Earthquakes;"))

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
    connection.execute(insert_query)
    count = connection.execute(
        text("SELECT COUNT(*) FROM Earthquakes;")).scalar()
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

    for name, query in queries.items():
        print(f"\n--- Executing query: {name} ---")
        result = connection.execute(text(query))
        if query.strip().lower().startswith("select"):
            rows = result.fetchall()
            for row in rows[:10]:
                print(row)
        else:
            print("Query executed successfully (no result to display).")

    output_path = "Earthquakes_export.csv"
    df_export = pd.read_sql(
        "SELECT * FROM Earthquakes", con=engine)
    df_export.to_csv(output_path, index=False, encoding='utf-8-sig')


run_database_final()
