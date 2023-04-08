import pandas as pd

path = "../data/saxion/"
activities = pd.read_parquet(path+'activities.parquet')

print(activities.head(3))

# Save the dataframe to a CSV file
activities_sample = activities.head(100)
activities_sample.to_csv(path+'activities_sample.csv', index=False)