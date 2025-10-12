import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# csv files list
csv_files = [
    "JAPAN_USGS.csv",
    "JAPAN_EMSC.csv",
    "JAPAN_DATASET.csv",
    "JAPAN_GEOFON.csv"
]
for f in csv_files:
    # task1 read
    df = pd.read_csv(f)
    # task2 shape
    print("Number of rows and columns:", df.shape)

    # rename columns
    
    if "date_and_time" in df.columns:
        df.rename(columns = {"date_and_time": "time"}, inplace = True)

    if "magnitude" in df.columns:
        df.rename(columns = {"magnitude": "mag"}, inplace = True)

    if "region" in df.columns:
        df.rename(columns = {"region": "place"}, inplace = True)

    

    #task3 convert datetime
    def convert_datetime(series):

        try:
            return pd.to_datetime(series, format = "%m/%d/%Y %I:%M:%S %p", errors = "coerce")
        except:
            pass

        try: # ISO format
            return pd.to_datetime(series, format = "%Y-%m-%dT%H:%M:%S.%fZ", errors = "coerce")
        except:
            pass
        return pd.to_datetime(series, errors = "coerce")
    df["time"] = convert_datetime(df["time"])
    
    #task3 conver float
    numeric_columns = []
    for column in df.columns:  
        try:
            df[column].astype(float)
            numeric_columns.append(column)
        except:
            pass
        
    float_columns = ["latitude", "longitude", "mag", "depth"] # must be floats

    all_float_columns = list(set(numeric_columns + float_columns)) 

    for column in all_float_columns:
        df[column] = pd.to_numeric(df[column], errors = "coerce").astype(float)
        
    # clean data (logical filters)
    
    df.loc[(df["mag"] < 0) | (df["mag"] > 10), "mag"] = pd.NA # 0 < Magnitude < 10
    
    df.loc[(df["depth"] < 0) | (df["depth"] > 700), "depth"] = pd.NA  # 0 < Depth < 700
    
    df.loc[df["latitude"] < 0, "latitude"] = pd.NA # latitude +
    df.loc[df["longitude"] < 0, "longitude"] = pd.NA # longitude +

    #task4 NaN values
    def missing_values(df):
        df = df.dropna(subset = ["time", "latitude", "longitude"]) # drop NaN time, latitude and longitude
       
        for column in ["mag", "depth"]:
            if column in df.columns:
                mean_dm = df[column].mean(skipna = True)
                df[column] = df[column].fillna(mean_dm) # replace NaN mag and depth with mean 

        df = df.fillna(0) # fill remaining (0)
        return df
    df = missing_values(df)
    
    #task5 month column
    
    df["time"] = pd.to_datetime(df["time"], errors = "coerce") #NaT

    df["month"] = df["time"].dt.month

    #task6 category column
    def categorize(mag):
        if mag < 4:
            return "Weak"      
        elif mag < 6:
            return "Moderate"   
        else:
            return "Strong"     

    df["category"] = df["mag"].apply(categorize)

    #task7 group by and calculate
    pivot = pd.pivot_table(
        df,
        values = "mag",
        index = "month",
        columns = "category",
        aggfunc = ["mean", "count"],
        fill_value = 0
    )

    print(pivot)

    #task8 extract region
    df["region"] = df["place"].copy()
    df["region"] = df["region"].str.lower()
    df = df.drop_duplicates()

    #task9
    pivot_region = pd.pivot_table(
        df,
        values = ["mag", "depth"],
        index = "region",
        aggfunc = ["count", "mean", "max"],
        fill_value = 0
    )
    print(pivot_region)

    pivot_region["count"]["mag"].plot(
    kind = "bar",
    figsize = (12,6),
    color= "green",
    title= "Earthquakes per Region"
    )
    plt.xlabel("Region")
    plt.ylabel("Number of Earthquakes")
    plt.show() 
    
















    

 









        


