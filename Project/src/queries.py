import pandas as pd
from pandasql import sqldf

teacher_work_hours_per_day = """
SELECT teachers.teacher AS Teacher, SUM(activities.duration) AS Minutes, activities.date AS daynr
FROM activities, teachers
WHERE teachers.course = activities.course
GROUP BY activities.date, teachers.teacher
HAVING SUM(activities.duration) > 480
"""


room_occupancy = """
SELECT activities.room AS roomcode, WEEK(activities.date) AS Weeknr, SUM(activities.duration) AS used_minutes ,YEAR(activities.date) AS yearnr
FROM activities
GROUP BY YEAR(activities.date), WEEK(activities.date), activities.room
HAVING SUM(activities.duration) > 1680
"""


def get_overworked_teachers(dataframe):
    # Convert time_start and time_end to datetime
    dataframe['time_start'] = pd.to_datetime(dataframe['time_start'])
    dataframe['time_end'] = pd.to_datetime(dataframe['time_end'])

    # Calculate duration in minutes and drop duplicate rows based on 'name', 'date', and 'course'
    dataframe['duration_minutes'] = (dataframe['time_end'] - dataframe['time_start']).dt.total_seconds() / 60
    dataframe = dataframe.drop_duplicates(subset=['name', 'date', 'course'])

    # Group by 'teacher', 'teacher_lastname', and 'date', then sum the 'duration_minutes'
    grouped_df = dataframe.groupby(['teacher', 'teacher_lastname', 'date'])['duration_minutes'].sum().reset_index()

    # Drop rows where 'teacher' equals 'EXTERN'
    grouped_df = grouped_df.loc[grouped_df['teacher'] != 'EXTERN']

    # Filter the results for more than 8 hours (480 minutes) per day
    result = grouped_df[grouped_df['duration_minutes'] > 480]

    # Display the result
    return result

def get_overtime(df):
    # Group the data by teacher and teacher_lastname
    grouped = df.groupby(['teacher', 'teacher_lastname'])

    # Calculate the total minutes worked and the number of days worked for each teacher
    total_minutes = grouped['duration_minutes'].sum()
    num_days_worked = grouped['date'].nunique()

    # Subtract 480 minutes from the total minutes worked
    extra_minutes = total_minutes - (num_days_worked * 480)

    # Calculate the average extra minutes worked per day
    avg_extra_minutes_per_day = extra_minutes / num_days_worked

    # Merge the results back to the original dataframe
    total_minutes.name = 'total_minutes_worked'
    avg_extra_minutes_per_day.name = 'avg_extra_minutes_per_day'


    result_df = pd.merge(df, total_minutes, on=['teacher', 'teacher_lastname'])
    result_df = pd.merge(result_df, avg_extra_minutes_per_day, on=['teacher', 'teacher_lastname'])

    # Rename the columns
    result_df = result_df.rename(columns={'duration_minutes': 'total_minutes_worked',
                                          0: 'avg_extra_minutes_per_day'})
    result_df.drop_duplicates(subset=['teacher', 'teacher_lastname'], inplace=True)


    return result_df


def get_room_occupancy(dataframe):
    dataframe['time_start'] = pd.to_datetime(dataframe['time_start'])
    dataframe['time_end'] = pd.to_datetime(dataframe['time_end'])

    unique_data = dataframe.drop_duplicates(subset=['date', 'room', 'time_start', 'time_end'])


    grouped_data = unique_data.groupby(['date', 'room'])['duration'].sum().reset_index()
    return grouped_data

def get_room_occupancy_info(dataframe):
    # Convert date column to datetime
    dataframe['date'] = pd.to_datetime(dataframe['date'])
    
    # Calculate total room usage
    room_usage = dataframe.groupby('room')['duration'].sum().reset_index()

    # Calculate the number of educational days per room per year
    dataframe['year'] = dataframe['date'].dt.year
    educational_days_per_year = 200
    room_year_counts = dataframe.groupby(['room', 'year'])['date'].nunique().reset_index()
    room_year_counts.rename(columns={'date': 'days_count'}, inplace=True)
    room_year_counts['available_time'] = room_year_counts['days_count'] * 480

    # Calculate the maximum available time for each room
    room_total_available_time = room_year_counts.groupby('room')['available_time'].sum().reset_index()

    # Calculate occupancy percentage
    room_info = pd.merge(room_usage, room_total_available_time, on='room')
    room_info['occupancy_percentage'] = (room_info['duration'] / room_info['available_time'] * 100).round(1)

    # Calculate room usage variance
    room_usage_by_day = dataframe.groupby(['room', 'date'])['duration'].sum().reset_index()
    room_usage_variance = (room_usage_by_day.groupby('room')['duration'].var().reset_index()).round()
    room_usage_variance.rename(columns={'duration': 'variance'}, inplace=True)

    # Merge the two dataframes
    room_info = pd.merge(room_info, room_usage_variance, on='room')

    # Filter rooms with occupancy >= 70%
    high_occupancy_rooms = room_info[room_info['occupancy_percentage'] >= 70]

    return high_occupancy_rooms, room_info