import pandas as pd

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
    teacher_workload = teacher_workload.pivot_table(index='year', columns='teacher_lastname', values='average_hours_worked', fill_value=0)

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