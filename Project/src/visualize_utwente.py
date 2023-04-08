import pandas as pd

path = "../data/utwente/"
activities = pd.read_parquet(path+'activities.parquet')
teachers = pd.read_parquet(path+'teachers.parquet')

print(activities.head(3))
print(teachers.head(3))
