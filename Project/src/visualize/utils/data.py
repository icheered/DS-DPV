import os
import pandas as pd

from utwente import WRITEMODE, TESTMODE

path = "../../data/utwente/"

def load_data():
    """
    Load data from parquet files

    test: bool
        If True, load only a subset of the data to speed things up
    """

    if TESTMODE:
        n_rows_to_load_activities = 1000
        n_rows_to_load_teachers = 1000
        activities = load_random_subset(path+'activities.parquet', n_rows_to_load_activities)
        teachers = load_random_subset(path+'teachers.parquet', n_rows_to_load_teachers)
    else: 
        activities = pd.read_parquet(path+'activities.parquet')
        teachers = pd.read_parquet(path+'teachers.parquet')

    return activities, teachers

def load_random_subset(file_path, n_rows_to_load):
    # Check if a random subset has already been generated for this file (filename+SUBSET+n_rows_to_load.parquet)
    # If so, load that subset
    # If not, generate a random subset and save it to disk
    
    filename, extension = os.path.splitext(file_path)
    subset_path = f"{filename}_SUBSET_{n_rows_to_load}{extension}"
    
    if os.path.exists(subset_path):
        # Load existing subset from disk
        data = pd.read_parquet(subset_path)
    else:
        # Generate and save new random subset
        data = pd.read_parquet(file_path)
        data = data.sample(n=n_rows_to_load, random_state=42)
        data.to_parquet(subset_path)
    
    return data

intermediate_output = '../../intermediate/utwente/'

def store_dataframe_to_csv(df, var_name):  
    if not WRITEMODE:
        return  
    # create the file path and filename
    file_path = intermediate_output + var_name + '.csv'
    
    # write dataframe to csv
    df.to_csv(file_path, index=True)
