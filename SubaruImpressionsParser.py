import csv
from collections import defaultdict



#i_file_name = sys.argv[1]
i_file_name = 'SubaruSpend.csv'
i_f = open(i_file_name)

reader = csv.reader(i_f)

# We do not make any changes to the input file obtained from the client
# This is very important because we will be receiving same file format
# in the future also
# I could have easily deleted the first 3 rows but I did not
# First 3 rows are not to be ignored

dump = reader.next()
dump = reader.next()
dump = reader.next()

# The forth row is the actual header
header = reader.next()

print header

num_weeks = len(header) - 4
weeks = header[4:num_weeks]

prev_line_2 = ""
prev_line_1 = ""


weekly_values = defaultdict(list)
monthly_values = defaultdict(list)

for line in reader:

    # logic for construction of key (look for leading and ending __
    # if the line[2] is blank, use the previous values stored in prev_ variable
    # Construction of key variables which will be used as unique id later on
    
    if line[1] != "":
        prev_line_1 = line[1].replace(" ","_")
    
    if line[2] != "":
        prev_line_2 = line[2].replace(" ","_")
        
    
    if line[3] == "":
        if line[2] == "":
            key =  prev_line_1
        else:
            key =  prev_line_1 +"_"+ prev_line_2
    else:        
        key =  prev_line_1 + "_" + prev_line_2 + "_" + line[3].replace(" ","_")
        
    print key

    
    # Once the key is constructed, we need to store the time series values
    # We have weekly numbers, we store both weekly and monthly numbers
    # in two data structures


    # Store the weekly time series

    for i in range(4,num_weeks):

        if key not in weekly_values.keys():
            weekly_values[key] = {}
            
        if line[i] == "":
            weekly_values[key][weeks[i-4]] = 0.0
        else:
            weekly_values[key][weeks[i-4]] = float(line[i])
        

        # Monthly values being calculated and stored in another data structure
        
        if key not in monthly_values.keys():
            monthly_values[key] = {}

        key_month_yyyy = str(weeks[i-4].split("/")[2])
        key_month_mm = str(weeks[i-4].split("/")[1])

        # In some cases 09 is 9, etc..take care of those instances

        if len(key_month_mm) == 2 and key_month_mm[0] == "0":
            key_month_mm = key_month_mm[1]

        #key_month = str(weeks[i-4].split("/")[2]) + str(weeks[i-4].split("/")[1])

        key_month = key_month_yyyy + key_month_mm

        if key_month not in  monthly_values[key].keys():
            monthly_values[key][key_month]= 0.0
            
        if line[i] == "":
            # store the months in format YYYYMM
            
            #key_month = str(weeks[i-4].split("/")[2]) + str(weeks[i-4].split("/")[1])

            #if monthly_values[key][key_month]:
            monthly_values[key][key_month] += 0.0

            #else:
            #monthly_values[key][key_month]  = 0.0
            
        else:
            #key_month = str(weeks[i-4].split("/")[2]) + str(weeks[i-4].split("/")[1])

            monthly_values[key][key_month] += float(line[i])
            
