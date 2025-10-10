import pandas as pd
import matplotlib.pyplot as plt

#task1 read
df = pd.read_csv("earthquake1.csv")

#task2 shape
print("Number of rows and columns:", df.shape)

#task3 data type & convert
df['time'] = pd.to_datetime(df['time'], errors='ignore')


numeric_columns = []
for column in df.columns:  
    try:
        df[column].astype(float)
        numeric_columns.append(column)
    except:
        pass

for column in numeric_columns:
    df[column] = df[column].astype(float)

#task4 nan values
df[numeric_columns] = df[numeric_columns].dropna()

#task5 month column
df['month'] = df['time'].dt.month

#task6 category column
def categorize(magnitude):
    if magnitude < 4:
        return 'Weak'      
    elif magnitude < 6:
        return 'Moderate'   
    else:
        return 'Strong'     

df['category'] = df['magnitude'].apply(categorize)

#task7 groupby & calculate
pivot = pd.pivot_table(
    df,
    values='magnitude',
    index='month',
    columns='category',
    aggfunc=['mean', 'count']
    )

print(pivot)


#task8 extract region 



#task9 region

Region = df.groupby('region')

#part1
earthquake_count = Region.size()
print("Number of earthquakes per region:")
print(earthquake_count)

#part2
mean_depth_mag = Region[['depth', 'magnitude']].mean()
print("Average depth and magnitude per region:")
print(mean_depth_mag)

#part3
max_depth_mag = Region[['depth', 'magnitude']].max()
print("Maximum depth and per region:")
print(max_depth_mag)

#part4
earthquake_count.plot( kind = "bar", figsize=(12, 6), title = "Earthquakes per Region", color = "green" )
plt.xlabel("Region")
plt.ylabel("Number of Earthquakes")
plt.show()








