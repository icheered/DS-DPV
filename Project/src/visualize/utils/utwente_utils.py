import pandas as pd
import os

intermediate_output = '../../intermediate/utwente/'
path = "../../data/utwente/"

def load_data(test=False):
    """
    Load data from parquet files

    test: bool
        If True, load only a subset of the data to speed things up
    """

    if test:
        n_rows_to_load_activities = 10000
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


def calculate_average_class_size(activities: pd.DataFrame) -> pd.DataFrame:
    # Filter out activities with a size of 0
    activities = activities[activities['size'] > 0]

    # Extract the year from the "date" column and add it as a new column "year"
    activities['year'] = pd.to_datetime(activities['date']).dt.year

    # Group the activities by year, date, time_start, and course code, then sum the sizes
    grouped_activities = activities.groupby(['year', 'date', 'time_start', 'coursecode']).agg(
        total_students=pd.NamedAgg(column='size', aggfunc='sum')
    ).reset_index()

    # Group the summed activities data by year and calculate the total number of students and classes
    yearly_activities = grouped_activities.groupby('year').agg(
        total_students=pd.NamedAgg(column='total_students', aggfunc='sum'),
        total_classes=pd.NamedAgg(column='coursecode', aggfunc='count')
    )

    # Calculate the average class size for each year
    yearly_activities['average_class_size'] = yearly_activities['total_students'] / yearly_activities['total_classes']
    
    return yearly_activities[['total_students', 'total_classes', 'average_class_size']]


def calculate_class_type_distribution(activities: pd.DataFrame) -> pd.DataFrame:
    # Extract the year from the "date" column and add it as a new column "year"
    activities['year'] = pd.to_datetime(activities['date']).dt.year

    # Group the activities data by year and class type
    grouped_activities = activities.groupby(['year', 'type']).size().reset_index(name='count')

    # Pivot the grouped data to have years as index, class types as columns, and counts as values
    class_type_distribution = grouped_activities.pivot_table(index='year', columns='type', values='count', fill_value=0)

    return class_type_distribution

def calculate_study_class_type_distribution(activities: pd.DataFrame) -> pd.DataFrame:
    # Extract the year from the "date" column and add it as a new column "year"
    activities['year'] = pd.to_datetime(activities['date']).dt.year

    # Group the activities data by year, study, and class type
    grouped_activities = activities.groupby(['year', 'study', 'type']).size().reset_index(name='count')

    # Pivot the grouped data to have years and study as index, class types as columns, and counts as values
    study_class_type_distribution = grouped_activities.pivot_table(index=['year', 'study'], columns='type', values='count', fill_value=0)

    return study_class_type_distribution

def calculate_total_duration_per_class_type(activities: pd.DataFrame) -> pd.DataFrame:
    # Extract the year from the "date" column and add it as a new column "year"
    activities['year'] = pd.to_datetime(activities['date']).dt.year

    # Group the activities data by year and class type, and sum the durations
    grouped_activities = activities.groupby(['year', 'type']).agg(
        total_duration=pd.NamedAgg(column='duration', aggfunc='sum')
    )

    # Convert total_duration from minutes to hours
    grouped_activities['total_duration'] = grouped_activities['total_duration'] / 60

    # Reset the index to bring 'year' and 'type' back as columns
    grouped_activities.reset_index(inplace=True)

    # Pivot the grouped data to have years as index, class types as columns, and total_duration as values
    total_duration_per_class_type = grouped_activities.pivot_table(index='year', columns='type', values='total_duration', fill_value=0)

    return total_duration_per_class_type


def calculate_teacher_workload(activities: pd.DataFrame, teachers: pd.DataFrame) -> pd.DataFrame:
    # Filter out activities with empty date field
    activities = activities[activities['date'].notnull()]

    # Extract the year from the "date" column and add it as a new column "year"
    activities['year'] = pd.to_datetime(activities['date']).dt.year

    teachers['course'] = teachers['course'].astype(str)
    activities['course'] = activities['course'].astype(str)

    # Join the Activities and Teachers datasets based on the course code and teacher ID
    merged = pd.merge(activities, teachers, left_on=['course', 'year'], right_on=['course', 'year'])

    # Group the data by year and teacher, and sum the duration to get the total number of hours worked by each teacher in each year
    teacher_workload = merged.groupby(['year', 'teacher'])['duration'].sum().reset_index(name='total_duration')

    # Join with the Teachers dataset to get the teacher's last name
    teacher_workload = pd.merge(teacher_workload, teachers[['teacher', 'teacher_lastname']], on=['teacher'])

    # Calculate the average number of hours worked by each teacher (assuming all teachers assigned to a course share the workload equally)
    teacher_workload['num_teachers'] = merged.groupby(['year', 'teacher'])['teacher'].transform('count')
    teacher_workload['average_hours_worked'] = (teacher_workload['total_duration']/60) / teacher_workload['num_teachers']

    # Pivot the data to have years as index, teacher last names as columns, and average number of hours worked as values
    teacher_workload = teacher_workload.pivot_table(index='year', columns='teacher_lastname', values='average_hours_worked')

    return teacher_workload



def calculate_teacher_class_type_distribution(activities: pd.DataFrame, teachers: pd.DataFrame) -> pd.DataFrame:


    # Extract the year from the "date" column and add it as a new column "year"
    activities['year'] = pd.to_datetime(activities['date']).dt.year
    
    # Filter out activities with empty date field
    activities = activities.dropna(subset=['date'])

    teachers['course'] = teachers['course'].astype(str)
    activities['course'] = activities['course'].astype(str)
    
    # Merge activities with teachers to get teacher names
    activities = activities.merge(teachers, on=['year', 'course'])

    # Group the activities data by year, class type, and teacher
    grouped_activities = activities.groupby(['year', 'type', 'teacher']).size().reset_index(name='count')
    
    # Calculate total workload for each teacher per year
    teacher_workload = grouped_activities.groupby(['year', 'teacher'])['count'].sum().reset_index(name='total_workload')

    # Merge the grouped data with teacher workload data
    grouped_activities = grouped_activities.merge(teacher_workload, on=['year', 'teacher'])

    # Calculate the proportion of time spent by each teacher on each class type
    grouped_activities['proportion'] = grouped_activities['count'] / grouped_activities['total_workload']

    # Pivot the grouped data to have years as index, class types as columns, and proportion values as values
    class_type_distribution = grouped_activities.pivot_table(index='year', columns='type', values='proportion', fill_value=0)
    
    return class_type_distribution


def calculate_teacher_activity_distribution(activities: pd.DataFrame, teachers: pd.DataFrame) -> pd.DataFrame:

    # Extract the year from the "date" column and add it as a new column "year"
    activities['year'] = pd.to_datetime(activities['date']).dt.year
    
    # Filter out activities with empty date field
    activities = activities.dropna(subset=['date'])

    teachers['course'] = teachers['course'].astype(str)
    activities['course'] = activities['course'].astype(str)

    # Join the activities and teachers dataframes based on the course code
    data = pd.merge(activities, teachers, left_on=['course', 'year'], right_on=['course', 'year'])
    

    # Group the data by year and teacher, and count the number of unique activities for each teacher in each year
    grouped_data = data.groupby(['year', 'teacher']).agg({'name': pd.Series.nunique}).reset_index()
    grouped_data = grouped_data.rename(columns={'name': 'activity_count'})
    
    # Pivot the data to have years as index, teachers as columns, and activity counts as values
    teacher_activity_distribution = grouped_data.pivot_table(index='year', columns='teacher', values='activity_count', fill_value=0)
    
    return teacher_activity_distribution

def calculate_room_distribution(activities: pd.DataFrame) -> pd.DataFrame:
    # Extract the year from the "date" column and add it as a new column "year"
    activities['year'] = pd.to_datetime(activities['date']).dt.year

    # Group the activities data by year and room
    grouped_activities = activities.groupby(['year', 'room']).size().reset_index(name='count')

    # Pivot the grouped data to have years as index, rooms as columns, and counts as values
    room_distribution = grouped_activities.pivot_table(index='year', columns='room', values='count', fill_value=0)

    # Sort the columns by total usage across all years, from most to least used
    room_distribution = room_distribution.reindex(sorted(room_distribution.sum().index, key=lambda x: -room_distribution.sum()[x]), axis=1)

    return room_distribution

def calculate_room_time(activities: pd.DataFrame) -> pd.DataFrame:
    # Extract the year from the "date" column and add it as a new column "year"
    activities['year'] = pd.to_datetime(activities['date']).dt.year

    # Convert the "duration" column from minutes to hours
    activities['hours'] = activities['duration'] / 60

    # Calculate the total time spent in each room for each year
    grouped_activities = activities.groupby(['year', 'room'])['hours'].sum().reset_index(name='total_time')

    # Pivot the grouped data to have years as index, rooms as columns, and total time as values
    room_time = grouped_activities.pivot_table(index='year', columns='room', values='total_time', fill_value=0)

    # Sort the columns by total time across all years, from most to least used
    room_time = room_time.reindex(sorted(room_time.sum().index, key=lambda x: -room_time.sum()[x]), axis=1)

    return room_time


import matplotlib.pyplot as plt

def calculate_activity_distribution(activities: pd.DataFrame) -> pd.DataFrame:
    # Extract the year and time from the "time_start" column and add them as new columns
    activities['year'] = pd.to_datetime(activities['time_start']).dt.year
    activities['time'] = pd.to_datetime(activities['time_start']).dt.time

    # Group the activities data by year and time
    grouped_activities = activities.groupby(['year', 'time']).size().reset_index(name='count')

    # Pivot the grouped data to have years as index, times as columns, and counts as values
    activity_distribution = grouped_activities.pivot_table(index='year', columns='time', values='count', fill_value=0)

    # Normalize the data to percentages
    activity_distribution = activity_distribution.div(activity_distribution.sum(axis=1), axis=0)

    # Plot the distribution for each year
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title('Activity Distribution by Time of Day')
    ax.set_xlabel('Time')
    ax.set_ylabel('Percentage')
    ax.grid(True)
    for year in activity_distribution.index:
        ax.plot(activity_distribution.loc[year], label=year)
    ax.legend()
    plt.show()

    return activity_distribution

def calculate_hourly_distribution(activities: pd.DataFrame) -> pd.DataFrame:
    # Extract the year from the "date" column and add it as a new column "year"
    activities['year'] = pd.to_datetime(activities['date']).dt.year

    # Group the activities data by year and hour of day
    activities['hour'] = pd.to_datetime(activities['time_start']).dt.hour
    grouped_activities = activities.groupby(['year', 'hour']).size().reset_index(name='count')

    # Pivot the grouped data to have years as index, hours as columns, and counts as values
    hourly_distribution = grouped_activities.pivot_table(index='hour', columns='year', values='count', fill_value=0)

    # Calculate the total number of activities per hour for each year
    hourly_totals = hourly_distribution.sum(axis=0)

    # Normalize the hourly distribution by the total number of activities per year and per minute
    hourly_distribution = hourly_distribution.divide(hourly_totals, axis=1) / 60

    return hourly_distribution

from tqdm import tqdm
def calculate_activity_distribution(activities: pd.DataFrame) -> pd.DataFrame:
    activities = activities.dropna(subset=['date'])
    # Extract the year from the "date" column and add it as a new column "year"
    activities['year'] = pd.to_datetime(activities['date']).dt.year

    # Create a new DataFrame to store the counts of activities per hour for each year
    years = activities['year'].unique()
    years.sort()
    hourly_range = pd.date_range(start='00:00', end='23:00', freq='H').time
    activity_distribution = pd.DataFrame(index=hourly_range, columns=years, data=0)

    # Iterate through the activities and increment the counts for the respective years and hours
    
    for _, activity in tqdm(activities.iterrows(), total=len(activities)):
        start_hour = pd.to_datetime(activity['time_start']).round('H').time()
        end_hour = pd.to_datetime(activity['time_end']).round('H').time()
        activity_distribution.loc[start_hour:end_hour, activity['year']] += 1

    # Calculate the total number of activities for each year
    total_activities = activities.groupby('year').size()

    # Divide the activity counts by the total number of activities for each year to get the percentage
    for year in years:
        activity_distribution[year] = activity_distribution[year] / total_activities[year] * 100

    return activity_distribution


def plot_activity_distribution(activity_distribution: pd.DataFrame):
    activity_distribution.plot(figsize=(10, 6))
    plt.xlabel('Hour of the day')
    plt.ylabel('Percentage of active activities')
    plt.title('Activities Distribution by Hour and Year')
    plt.legend(title='Year')
    plt.xlim(pd.to_datetime('07:00').time(), pd.to_datetime('22:30').time())
    plt.grid()
    plt.show()

import calendar

def calculate_activity_distribution_by_day(activities: pd.DataFrame) -> pd.DataFrame:
    activities = activities.dropna(subset=['date'])
    # Extract the year from the "date" column and add it as a new column "year"
    activities['year'] = pd.to_datetime(activities['date']).dt.year

    # Create a new DataFrame to store the counts of activities per weekday for each year
    years = activities['year'].unique()
    years.sort()
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    activity_distribution = pd.DataFrame(index=weekdays, columns=years, data=0)

    # Iterate through the activities and increment the counts for the respective years and weekdays
    for _, activity in tqdm(activities.iterrows(), total=len(activities)):
        weekday = pd.to_datetime(activity['date']).strftime('%A')
        if weekday in weekdays:
            activity_distribution.loc[weekday, activity['year']] += 1

    # Calculate the total number of activities for each year
    total_activities = activities.groupby('year').size()

    # Divide the activity counts by the total number of activities for each year to get the percentage
    for year in years:
        activity_distribution[year] = activity_distribution[year] / total_activities[year] * 100

    return activity_distribution

def plot_activity_distribution_by_day(activity_distribution: pd.DataFrame):
    activity_distribution.plot(figsize=(10, 6))
    plt.xlabel('Day of the week')
    plt.ylabel('Percentage of planned activities')
    plt.title('Activities Distribution by Day of the Week and Year')
    plt.legend(title='Year')
    plt.grid()
    plt.show()