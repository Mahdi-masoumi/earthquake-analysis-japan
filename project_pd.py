import pandas as pd
import matplotlib.pyplot as plt

#task1_read
df = pd.read_csv("earthquake1.csv")

#task2_shape
print(df.shape)

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



# 9. region

Region = df.groupby('region')

#part1
earthquake_count = Region.size()
print(earthquake_count)

#part2
mean_depth_mag = Region[['depth', 'magnitude']].mean()
print(mean_depth_mag)

#part3
max_depth_mag = Region[['depth', 'magnitude']].max()
print(max_depth_mag)

