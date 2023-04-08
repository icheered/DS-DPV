# Split the saxion inputdata into two files, because the original file is too large to be uploaded to github.
import csv

input_file = 'All timetabling activities SAX 2013-2015.csv'
output_file_1 = 'All_timetabling_activities_SAX_2013-2015_PART1.csv'
output_file_2 = 'All_timetabling_activities_SAX_2013-2015_PART2.csv'

# count the number of lines in the input file
num_lines = sum(1 for line in open(input_file))

# calculate the midpoint
midpoint = num_lines // 2

# open the input file
with open(input_file, 'r') as infile:
    # create two output files
    with open(output_file_1, 'w', newline='') as outfile1, open(output_file_2, 'w', newline='') as outfile2:
        # create CSV writers for the output files
        writer1 = csv.writer(outfile1)
        writer2 = csv.writer(outfile2)

        # loop through the input file
        for i, row in enumerate(csv.reader(infile)):
            # write the row to the appropriate output file
            if i < midpoint:
                writer1.writerow(row)
            else:
                writer2.writerow(row)
