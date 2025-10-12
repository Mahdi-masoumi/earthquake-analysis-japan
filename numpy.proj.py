import numpy as np
import pandas as pd

tokyo_long = 139.6500
tokyo_lat = 35.6764

x = df["longitude"].values
y = df["latitude"].values

df["tokyo_distance"] = np.sqrt((x - tokyo_long)**2 + (y - tokyo_lat)**2)

mags = df["mag"].values
mean_mag = np.mean(mags)
std_mag = np.std(mags)
percentiles_mag = np.percentile(mags, [25, 50, 75])

mean_distance = np.mean(df["tokyo_distance"])
std_distance = np.std(df["tokyo_distance"])
percentiles_distance = np.percentile(df["tokyo_distance"], [25, 50, 75])
