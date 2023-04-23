import pandas as pd

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