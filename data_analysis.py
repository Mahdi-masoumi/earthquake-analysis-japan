import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast 

d = "charts_output"
if not os.path.exists(d):
    try:
        os.makedirs(d, exist_ok=True)
    except:
        pass

df = pd.read_csv("Earthquakes_export.csv")

try:
    df["time"] = pd.to_datetime(df["time"], errors="coerce", utc=True)
except Exception as e:
    print("time parse err:", e)

try:
    df["time"] = df["time"].dt.tz_convert("UTC").dt.tz_localize(None)
except:
    try:
        df["time"] = df["time"].dt.tz_localize(None)
    except:
        pass
try:
    regs = df["region"].dropna().unique()
except:
    regs = []
    
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x="magnitude", hue="region", bins=10, multiple="stack", palette="tab10")
plt.title("Magnitude Distribution by Region")
plt.xlabel("Magnitude")
plt.ylabel("Count")
# plt.tight_layout()
plt.savefig(os.path.join(d, "combined_hist.png"))
plt.close()

try:
    df["date"] = df["time"].dt.date
except:
    df["date"] = pd.to_datetime(df["time"], errors="coerce").dt.date

cnt = df.groupby("date").size()
avg = df.groupby("date")["magnitude"].mean()

plt.figure()
plt.plot(cnt.index, cnt.values, label="count")
plt.plot(avg.index, avg.values, label="mean_mag")
plt.legend()
plt.xticks(rotation=45)
plt.title("daily count and avg magnitude")
plt.xlabel("date")
plt.ylabel("value")
plt.tight_layout()
plt.savefig(os.path.join(d, "line_daily.png"))
plt.close()

try:
    plt.figure()
    plt.scatter(df["depth"], df["magnitude"])
    plt.title("magnitude vs depth")
    plt.xlabel("depth")
    plt.ylabel("mag")
    plt.tight_layout()
    plt.savefig(os.path.join(d, "scatter_depth_mag.png"))
    plt.close()
except Exception as e:
    print("scatter depth/mag err:", e)

try:
    plt.figure()
    plt.scatter(df["time"], df["magnitude"])
    plt.title("magnitude vs time")
    plt.xlabel("time")
    plt.ylabel("mag")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(d, "scatter_time_mag.png"))
    plt.close()
except Exception as e:
    print("scatter time/mag err:", e)

try:
    df["depth_cat"] = pd.cut(df["depth"], [-1, 70, 300, 10000],
                             labels=["shallow", "intermediate", "deep"])
    a = df.loc[df["depth_cat"] == "shallow", "magnitude"].dropna()
    b = df.loc[df["depth_cat"] == "intermediate", "magnitude"].dropna()
    c = df.loc[df["depth_cat"] == "deep", "magnitude"].dropna()
    plt.figure()
    plt.boxplot([a, b, c])
    plt.xticks([1, 2, 3], ["shallow", "intermediate", "deep"])
    plt.title("mag distribution by depth category")
    plt.xlabel("depth category")
    plt.ylabel("mag")
    plt.tight_layout()
    plt.savefig(os.path.join(d, "boxplot_mag_depth_cat.png"))
    plt.close()
except Exception as e:
    print("boxplot err:", e)

try:
    df["coordination"] = df["coordination"].apply(ast.literal_eval)
    df["latitude"] = df["coordination"].apply(lambda x: x[0])
    df["longitude"] = df["coordination"].apply(lambda x: x[1])
    ll = df[["longitude", "latitude"]].dropna()
    plt.figure()
    plt.hist2d(ll["longitude"], ll["latitude"], bins=50)
    plt.colorbar()
    plt.title("heatmap of lat-long")
    plt.xlabel("longitude")
    plt.ylabel("latitude")
    plt.tight_layout()
    plt.savefig(os.path.join(d, "heatmap_lat_lon.png"))
    plt.close()
except Exception as e:
    print("heatmap err:", e)


#  [Index(['longitude', 'latitude'], dtype='object')] are in the [columns]"