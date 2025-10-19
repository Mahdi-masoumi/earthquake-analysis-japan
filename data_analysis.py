import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast

d = "charts_output"
os.makedirs(d, exist_ok=True)

df = pd.read_csv("Earthquakes_export.csv")

try:
    df["time"] = pd.to_datetime(df ["time"], errors="coerce", utc=True)
    df["time"] = df["time"].dt.tz_convert("UTC").dt.tz_localize(None)
except:
    try:
        df["time"] = df["time"].dt.tz_localize(None)
    except:
        pass

def plot_histogram (df, save_dir =d ):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x="magnitude", hue="region", bins=10, multiple="stack", palette="tab10")
    plt.title("Magnitude Distribution by Region")
    plt.xlabel("Magnitude")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "combined_hist.png"))
    plt.close()

def plot_line (df , save_dir = d, freq = "D"):
    df["date"] = df ["time"].dt.to_period ( freq ).dt.start_time
    cnt = df.groupby("date").size()
    avg = df.groupby("date") ["magnitude"].mean()

    plt.figure ()
    plt.plot(cnt.index, cnt.values , label="count")
    plt.plot(avg.index , avg.values, label="mean_mag")
    plt.legend ()
    plt.xticks(rotation=45)
    plt.title(f"{freq}-wise count and avg magnitude")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f"line_{freq}.png"))
    plt.close ()

def plot_scatter (df, x_col, y_col, save_name, save_dir=d):
    plt.figure ()
    plt.scatter (df[x_col], df[y_col])
    plt.title (f"{y_col} vs {x_col}")
    plt.xlabel (x_col)
    plt.ylabel (y_col)
    if x_col=="time":
        plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, save_name))
    plt.close()

def plot_boxplot (df, save_dir=d):
    df["depth_cat"] = pd.cut(df ["depth"], [-1, 70, 300, 10000],
                             labels=["shallow", "intermediate", "deep"])
    a = df.loc[df ["depth_cat"]=="shallow", "magnitude"].dropna()
    b = df.loc[df ["depth_cat"]=="intermediate", "magnitude"].dropna()
    c = df.loc[df ["depth_cat"]=="deep", "magnitude"].dropna()

    plt.figure()
    plt.boxplot([a, b, c])
    plt.xticks([1, 2, 3], ["shallow", "intermediate", "deep"])
    plt.title("Magnitude distribution by depth category")
    plt.xlabel("Depth category")
    plt.ylabel("Magnitude")
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "boxplot_mag_depth_cat.png"))
    plt.close()

def plot_heatmap (df, save_dir=d):
    df["coordination"] = df["coordination"].apply(ast.literal_eval)
    df["latitude"] = df["coordination"].apply (lambda x: x[0] )
    df["longitude"] = df["coordination"].apply(lambda x: x[1])

    ll = df[["longitude", "latitude"]].dropna ()
    plt.figure ()
    plt.hist2d(ll["longitude"], ll["latitude"], bins=50)
    plt.colorbar()
    plt.title("Heatmap of lat-long")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir,            "heatmap_lat_lon.png"))
    plt.close ()

plot_histogram (df)
plot_line(df, freq="D")
plot_scatter (df, "depth", "magnitude", "scatter_depth_mag.png")
plot_scatter (df, "time", "magnitude", "scatter_time_mag.png")
plot_boxplot (df)
plot_heatmap (df)
