import pandas as pd
from pandasql import sqldf 

path = "rawdata/utwente/"
activityfiles = ['activities_2013-2014.csv', 'activities_2014-2015.csv', 'activities_2015-2016.csv', 'activities_2016-2017.csv']
teacherfiles = ['teachers_2015.csv', 'teachers_2016.csv']
courseteacherfiles = ['course_teachers_2013-2014.csv', 'course_teachers_2014-2015.csv']

# Read and concatenate the activities dataframes
activities = pd.concat([pd.read_csv(path+file) for file in activityfiles], ignore_index=True)
activities = activities.rename(columns={
    "Naam-Activiteit": "name",
    "Beschrijving-Activiteit": "description",
    "Hostkey1": "hostkey1",
    "Hostkey2": "hostkey2",
    "Activiteitstype": "type",
    "Datum": "date",
    "Tijd van": "time_start",
    "Tijd tot en met": "time_end",
    "Grootte": "size",
    "Zaal-Activiteit": "room"
})

# There are 2 hostkey columns, one with the course code and one with the course name. Split into separate columns.
def split_hostkey(row):
    course = None
    coursecode = None

    for col in ['hostkey1', 'hostkey2']:
        if str(row[col]).startswith('#'):
            coursecode = row[col]
        else:
            course = row[col]

    return pd.Series([course, coursecode])

activities[['course', 'coursecode']] = activities.apply(lambda row: split_hostkey(row), axis=1)

# Drop the original 'hostkey' column
activities = activities.drop(columns=['hostkey1', 'hostkey2'])

# Remove lagging spaces from the time columns
activities['time_start'] = activities['time_start'].astype(str).apply(lambda x: x.strip())
activities['time_end'] = activities['time_end'].astype(str).apply(lambda x: x.strip())

activities.to_csv('data/utwente/activities.csv', index=False)


# Read and concatenate the teachers and course_teachers dataframes
teachersdf = pd.concat([pd.read_csv(path + file, usecols=['Cursus', 'Cursusnaam', 'Collegejaar', 'Medewerker']) for file in teacherfiles])
course_teachersdf = pd.concat([pd.read_csv(path + file, usecols=['Collegeyear', 'Course', 'Coursename', 'Teachernr', 'Teacher-lastname']) for file in courseteacherfiles])
teachersdf.rename(columns={'Cursus': 'Course', 'Cursusnaam': 'Coursename', 'Collegejaar': 'Collegeyear', 'Medewerker': 'Teachernr'}, inplace=True)
merged = pd.concat([course_teachersdf, teachersdf], axis=0, ignore_index=True)
teachers = merged[['Collegeyear', 'Course', 'Coursename', 'Teachernr', 'Teacher-lastname']]


teachers = teachers.rename(columns={
    "Collegeyear": "year",
    "Course": "course",
    "Coursename": "coursename",
    "Teachernr": "teacher",
    "Teacher-lastname": "teacher_lastname",
})

teachers.to_csv('data/utwente/teachers.csv', index=False)