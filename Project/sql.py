import pandas as pd
from pandasql import sqldf

# Read CSV file into a pandas dataframe
df = pd.read_csv('data.csv')

# Define SQL query
query = "SELECT * FROM df WHERE column1 > 5"

# Execute SQL query on the dataframe
result = sqldf(query)

# Print the result
print(result)
