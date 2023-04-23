import pandas as pd
import matplotlib.pyplot as plt
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
    print(activity_distribution)
    activity_distribution.plot(figsize=(10, 6))
    plt.xlabel('Hour of the day')
    plt.ylabel('Percentage of active activities')
    plt.title('Activities Distribution by Hour and Year')
    plt.legend(title='Year')
    plt.xlim(pd.to_datetime('08:00').time(), pd.to_datetime('22:00').time())
    plt.grid()
    plt.show()



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