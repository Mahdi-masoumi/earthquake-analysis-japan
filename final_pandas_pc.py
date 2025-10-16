import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# csv files list
csv_files = [
    "JAPAN_USGS.csv",
    "JAPAN_EMSC.csv",
    "JAPAN_DATASET.csv",
    "JAPAN_GEOFON.csv"
]

dataframes = []


for f in csv_files:
    # task1 read
    df = pd.read_csv(f)
    cleaned_df = df.copy()
    


    # task2 shape
    print("Number of rows and columns:", cleaned_df.shape)


    # rename columns
    if "coordinates" in cleaned_df.columns:
        cleaned_df["coordinates"] = cleaned_df["coordinates"].fillna("")
        coordinates = cleaned_df["coordinates"].str.split(",", expand = True)
        cleaned_df["longitude"] = coordinates[0].str.replace("°E", "").str.strip().astype(float)
        cleaned_df["latitude"] = coordinates[1].str.replace("°N", "").str.strip().astype(float)
        cleaned_df.drop(columns=["coordinates"], inplace = True)

   

    if "date_and_time" in cleaned_df.columns:
        cleaned_df.rename(columns = {"date_and_time": "time"}, inplace = True)

    if "magnitude" in cleaned_df.columns:
        cleaned_df.rename(columns = {"magnitude": "mag"}, inplace = True)

    if "region" in cleaned_df.columns:
        cleaned_df.rename(columns = {"region": "place"}, inplace = True)

    # print(cleaned_df.head(3))
    # print(cleaned_df.columns)

    

    #task3 convert datetime  

    formats = [ "%m/%d/%Y  %I:%M:%S %p", "%Y-%m-%dT%H:%M:%S.%fZ", "%m/%d/%Y %H:%M" ] 

    def convert_datetime(series):
        # df["time"] = df["time"].astype(str).str.strip()
        for f in formats:
            try:
                return pd.to_datetime(series, format = f)
            except:
                continue
        return pd.NaT
    cleaned_df["time"] = cleaned_df["time"].apply(convert_datetime)

    # print(cleaned_df["time"])
    
    #task3 conver float
    numeric_columns = []
    for column in cleaned_df.columns:  
        try:
            cleaned_df[column].astype(float)
            numeric_columns.append(column)
        except:
            pass
        
    float_columns = ["latitude", "longitude", "mag", "depth"] # must be floats

    all_float_columns = list(set(numeric_columns + float_columns)) 

    for column in all_float_columns:
        cleaned_df[column] = pd.to_numeric(cleaned_df[column], errors = "coerce")

    # print(cleaned_df.dtypes)
    # print(cleaned_df.head())

        
    # clean data (logical filters)
    
    cleaned_df.loc[(cleaned_df["mag"] < 0) | (cleaned_df["mag"] > 10), "mag"] = pd.NA # 0 < Magnitude < 10
    
    cleaned_df.loc[(cleaned_df["depth"] < 0) | (cleaned_df["depth"] > 700), "depth"] = pd.NA  # 0 < Depth < 700
    
    cleaned_df.loc[cleaned_df["latitude"] < 0, "latitude"] = pd.NA # latitude +

    cleaned_df.loc[cleaned_df["longitude"] < 0, "longitude"] = pd.NA # longitude +
    # print(cleaned_df[["time", "latitude", "longitude"]].isna().sum())

    # print(cleaned_df)

    #task4 NaN values
    def missing_values(cleaned_df):
        cleaned_df = cleaned_df.dropna(subset = ["time", "latitude", "longitude"]) # drop NaN time, latitude and longitude

        for column in ["mag", "depth"]:
            if column in cleaned_df.columns:
                mean_dm = cleaned_df[column].mean(skipna=True)
                cleaned_df.loc[:, column] = cleaned_df[column].fillna(mean_dm)

            cleaned_df = cleaned_df.fillna(0) # fill remaining (0)
        return cleaned_df
    cleaned_df = missing_values(cleaned_df)
    # print(cleaned_df.head(4))
    # print(cleaned_df[["time", "latitude", "longitude"]].isna().sum())
   
    
    # #task5 month column
    
    cleaned_df["time"] = pd.to_datetime(cleaned_df["time"], errors = "coerce") 
    cleaned_df["month"] = cleaned_df["time"].dt.month
    

#task6 category column
    def categorize(mag):
        if mag < 4:
            return "Weak"      
        elif mag < 6:
            return "Moderate"   
        else:
            return "Strong"     

    cleaned_df["category"] = cleaned_df["mag"].apply(categorize)

    # print(cleaned_df["month"])
    # print(cleaned_df["category"])
    


    #task7 group by and calculate
    pivot = pd.pivot_table(
        cleaned_df,
        values = "mag",
        index = "month",
        columns = "category",
        aggfunc = ["mean", "count"],
        fill_value = 0
    )

    print(pivot)

    #task8 extract region
    def extract_usgs(place):
        if not isinstance(place, str) or place.strip() == "":
            return "Not Found"

        elif ", Japan region" in place:
            return place.replace(", Japan region", "").strip()
        
        elif "km" in place:
            region_format = re.search(r'of\s+([^,]+),\s*Japan', place)
            if region_format:
                return region_format.group(1).strip()
            else:
                return "Not Found"
        else:
            return "Not Found"


    def extract_emsc_geofon(place):
        if not isinstance(place, str) or place.strip() == "":
            return "Not Found"
        
        place = place.lower()
        
        invalid_regions = ["south korea", "yellow sea"]
        if place in invalid_regions:
            return "Not Found"
        
        if place.strip() == "eastern sea of japan":
            return "Eastern Sea Of Japan"
        
        removing_words = ["off", "near", "western", "eastern", "east", "west", "north", "south", "coast of", "region", "japan"]
        for w in removing_words:
            place = place.replace(w, "")
        cleaned_place = place.strip()
        
        if cleaned_place == "":
            return "Not Found"
        
        return cleaned_place.title()

    def extract_dataset(place):
        
        if not isinstance(place, str) or place.strip() == "":
            return "Not Found"
        
        if "sea of japan" in place.lower():
            return "Sea Of Japan"

        removing_words = [
            "off", "near", "offshore", "central",
            "east", "west", "north", "south",
            "coast of", "region", "prefecture",
            "japan", "ryukyu islands"
        ]

        cleaned_place = place.lower()
        for w in removing_words:
            cleaned_place = cleaned_place.replace(w, "")
        
        cleaned_place = cleaned_place.strip()

        if cleaned_place == "":
            return "Not Found"
        
        return cleaned_place.title()

    cleaned_df["region"] = cleaned_df["place"].copy()

    if f == "JAPAN_USGS.csv":
        cleaned_df["region"] = cleaned_df["region"].apply(extract_usgs) 
    elif f == "JAPAN_EMSC.csv":
        cleaned_df["region"] = cleaned_df["region"].apply(extract_emsc_geofon)  
    elif f == "JAPAN_DATASET.csv":
        cleaned_df["region"] = cleaned_df["region"].apply(extract_dataset)  
    elif f == "JAPAN_GEOFON.csv":
        cleaned_df["region"] = cleaned_df["region"].apply(extract_emsc_geofon)

    # print(cleaned_df.head(7))

    #task9
    earthquake_count = cleaned_df.groupby("region").size()
    print(earthquake_count)

    earthquake_mean = cleaned_df.groupby("region")[["mag", "depth"]].mean()
    print(earthquake_mean) 

    earthquake_max = cleaned_df.groupby("region")[["mag", "depth"]].max()
    print(earthquake_max)

    earthquake_count.plot.bar(
        color = "blue",
        title = "Earthquakes per Region",
        xlabel= "Region",
        ylabel = "Number of Earthquakes",
        figsize = (12, 6)
    )

    plt.show() 
    dataframes.append(cleaned_df)
    # print(dataframes)

all_dfs = pd.concat(dataframes, ignore_index = True)
all_dfs.to_csv("earthquake_cleaned.csv")

    
















    

 









        
