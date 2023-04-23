import visualize.utwente_utils.utwente_utils as utils





def main():
    activities, teachers = utils.load_data()


    pass

if __name__ == '__main__':
    main()










import pandas as pd
from pandasql import sqldf

from queries import teacher_work_hours_per_day, room_occupancy, get_overworked_teachers, get_overtime, get_room_occupancy, get_room_occupancy_info

intermediate_output = '../../intermediate/utwente/'

# Import data
path = "../../data/utwente/"
data = pd.read_parquet(path+'activities.parquet')

# # ## Get overworked teachers
# # # results = get_overworked_teachers(data)
# # # results.to_csv('overworked_teachers.csv', index=False)

# # # unique_lastnames = results['teacher_lastname'].unique()

# # # print(len(unique_lastnames), unique_lastnames)



# Get stats on overworked teachers
# overworked_teachers  = pd.read_csv(intermediate_output+'overworked_teachers.csv')
# overtime = get_overtime(overworked_teachers)
# overtime.sort_values(by='avg_extra_minutes_per_day', ascending=False, inplace=True)
# overtime.to_csv(intermediate_output+'overtime.csv', index=False)


# Get stats on room occupancy
room_occupancy = get_room_occupancy(data).sort_values(by='duration')
less_frequent_high_usage_rooms, room_info = get_room_occupancy_info(room_occupancy)

room_info.sort_values(by='occupancy_percentage', ascending=False, inplace=True)
room_info.to_csv(intermediate_output+'room_info.csv', index=False)

less_frequent_high_usage_rooms.sort_values(by='occupancy_percentage', ascending=False, inplace=True)
less_frequent_high_usage_rooms.to_csv(intermediate_output+'less_frequent_high_usage_rooms.csv', index=False)


