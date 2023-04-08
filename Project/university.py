import pandas as pd
from pandasql import sqldf 

path = "data/utwente/"
activityfiles = ['activities_2013-2014.csv', 'activities_2014-2015.csv', 'activities_2015-2016.csv', 'activities_2016-2017.csv']
teacherfiles = ['teachers_2015.csv', 'teachers_2016.csv']
courseteacherfiles = ['course_teachers_2013-2014.csv', 'course_teachers_2014-2015.csv']

# Read and concatenate the activities dataframes
activities = pd.concat([pd.read_csv(path+file) for file in activityfiles], ignore_index=True)
activities = activities.rename(columns={
    "Naam-Activiteit": "name",
    "Beschrijving-Activiteit": "description",
    "Hostkey": "hostkey",
    "Hostkey": "hostkey",
    "Activiteitstype": "type",
    "Datum": "date",
    "Tijd van": "time_start",
    "Tijd tot en met": "time_end",
    "Grootte": "size",
    "Zaal-Activiteit": "room"
})

# There are 2 hostkey columns, one with the course code and one with the course name. Split into separate columns.
def split_hostkey(row):
    if row['hostkey'].startswith('#'):
        return pd.Series({'course': '', 'coursecode': row['hostkey']})
    else:
        return pd.Series({'course': row['hostkey'], 'coursecode': ''})

activities[['course', 'coursecode']] = activities.apply(lambda row: split_hostkey(row), axis=1)

# Drop the original 'hostkey' column
activities = activities.drop('hostkey', axis=1)

activities.to_csv('activities_preprocessed.csv', index=False)


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

teachers.to_csv('teachers_preprocessed.csv', index=False)