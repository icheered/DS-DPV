import pandas as pd

path = "../data/saxion/"
activities = pd.read_parquet(path+'activities.parquet')

print(activities.head(3))