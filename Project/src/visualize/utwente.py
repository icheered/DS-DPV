import utils.activities as activities_planning
import utils.teacher as teacher
import utils.room as room
import utils.class_size_type as class_size_type
import utils.data as data

TESTMODE = False     # Set to True to only load a subset of the data to speed things up
WRITEMODE = False    # Set to True to write the output to disk

def main():
    activities, teachers = data.load_data()

    #################
    # CLASS
    #################
    print("Average class size")
    average_class_size = class_size_type.calculate_average_class_size(activities)
    print(average_class_size)
    data.store_dataframe_to_csv(average_class_size, "average_class_size")

    print("Average class size per class type")
    class_type_distribution = class_size_type.calculate_class_type_distribution(activities)
    print(class_type_distribution)
    data.store_dataframe_to_csv(class_type_distribution, "class_type_distribution")

    print("Average class size per class type and per study")
    study_class_type_distribution = class_size_type.calculate_study_class_type_distribution(activities)
    print(study_class_type_distribution)
    data.store_dataframe_to_csv(study_class_type_distribution, "study_class_type_distribution")

    print("Total duration per class type")
    total_duration_per_class_type = class_size_type.calculate_total_duration_per_class_type(activities)
    print(total_duration_per_class_type)
    data.store_dataframe_to_csv(total_duration_per_class_type, "total_duration_per_class_type")

    #################
    # TEACHERS
    #################
    print("Teacher workload")
    teacher_average_hours = teacher.calculate_teacher_workload(activities, teachers)
    print(teacher_average_hours)
    data.store_dataframe_to_csv(teacher_average_hours, "teacher_average_hours")

    print("Teacher workload per class type")
    teacher_activities = teacher.calculate_teacher_class_type_distribution(activities, teachers)
    print(teacher_activities)
    data.store_dataframe_to_csv(teacher_activities, "teacher_activities")

    print("Involement of teachers in activities")
    teacher_number_of_involvements = teacher.calculate_teacher_activity_distribution(activities, teachers)
    print(teacher_number_of_involvements)
    data.store_dataframe_to_csv(teacher_number_of_involvements, "teacher_number_of_involvements")

    #################
    # ROOMS
    #################

    print("Room usage by number of activities")
    room_usage_number_of_activities = room.calculate_room_distribution(activities)
    print(room_usage_number_of_activities)
    data.store_dataframe_to_csv(room_usage_number_of_activities, "room_usage_number_of_activities")

    print("Room usage by time")
    room_usage_time =  room.calculate_room_time(activities)
    print(room_usage_time)
    data.store_dataframe_to_csv(room_usage_time, "room_usage_time")

    #################
    # ACTIVITIES
    #################

    print("Distribution of activities throughout the day")
    activity_distribution = activities_planning.calculate_activity_distribution(activities)
    data.store_dataframe_to_csv(activity_distribution, "activity_distribution")
    activities_planning.plot_activity_distribution(activity_distribution)

    print("Distribution of activities per weekday")
    activity_distribution_day = activities_planning.calculate_activity_distribution_by_day(activities)
    data.store_dataframe_to_csv(activity_distribution_day, "activity_distribution_day")
    activities_planning.plot_activity_distribution_by_day(activity_distribution_day)


if __name__ == '__main__':
    main()