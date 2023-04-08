import pandas as pd

path = "../rawdata/saxion/"
outputpath = "../data/saxion/"
activityfiles = ['All_timetabling_activities_SAX_2013-2015_PART1.csv', 'All_timetabling_activities_SAX_2013-2015_PART2.csv']

# Read and concatenate the activities dataframes
activities = pd.concat([pd.read_csv(path+file) for file in activityfiles], ignore_index=True)

activities = activities.rename(columns={
    "DATE":"date",
    "START":"time_start",
    "END":"time_end",
    "ACADEMY":"academy",
    "PLACE":"place",
    "CLASS":"class",
    "EDUC.CODE1":"educode",
    "BISONCODE":"bisoncode",
    "NAME":"name",
    "TEACHER":"teacher",
    "NAMEFULL":"teacher_fullname",
    "ROOM":"room",
    "REMARKS":"remarks",
    "CALENDER_WEEK":"calendar_week",
    "QUARTILE_WEEK":"quartile_week",
    "QUARTILE":"quartile",
    "LESSONWEEK":"lesson_week",
    "ACTIVITY":"activity",
    "SCHOOLYEAR":"schoolyear",
})

# Turning time_start and time_end into datetime objects to calculate duration
activities['date'] = pd.to_datetime(activities['date'], errors='coerce')
activities['time_start'] = pd.to_datetime(activities['date'].astype(str) + ' ' + activities['time_start'], errors='coerce')
activities['time_end'] = pd.to_datetime(activities['date'].astype(str) + ' ' + activities['time_end'], errors='coerce')
activities['duration'] = (activities['time_end'] - activities['time_start']).dt.total_seconds().div(60)

# Save the combined DataFrame as a Parquet file
activities.to_parquet(outputpath+'activities.parquet', compression='snappy')

activities_sample = activities.head(100)
activities_sample.to_csv(outputpath+'activities_sample.csv', index=False)