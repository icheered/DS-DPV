import pandas as pd

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