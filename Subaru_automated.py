import csv
from datetime import *
from pandas import *
from collections import defaultdict
import collections
import subprocess
import sys

import numpy as np
import os


scores = dict()
time_series = defaultdict(list)
leadsGraph     =    dict()
lagsGraph      =    dict()

telstra = dict()
keys = []
finalOutputFileName = ''
finalOutputKeyName  = ''

def find_leading(key_pos):
    lead_key = []
    print leadsGraph['1'].keys()
    for lagger_key in leadsGraph[str(key_pos)].keys():
        if leadsGraph[str(key_pos)][lagger_key] > leadsGraph[lagger_key][str(key_pos)]:
            lead_key.append(lagger_key) 
    return lead_key


def calcLaggedCorrelation( s1, s2, lag):

    # Lengths have to be equal for correlation calculation
    if(len(s1) != len(s2)):
        return -1
    
    s1_trunc = s1[0:(len(s1)-lag)]
    s2_trunc = s2[lag:(len(s1))]

    # Correlations undefined in such scenario
    if (len(s1_trunc) <1 ):
        return -1
    
    corrMat = np.corrcoef(s1_trunc, s2_trunc)

    return corrMat[0,1]



# Function to calculate aggregated lagged correlations
# between two time series
# if lead =1, s1 is leading
# pos indicates whether to calculate positive or negative corr

def calcAggregatedCorrelation( s1, s2, numLags, lead, pos):
    sumCorr = 0.0
    if (lead == 0):
        for i in range(0, numLags):
            corr = calcLaggedCorrelation(s1, s2, i)
      #     print corr
            if (pos == 1):
                sumCorr += max(corr,0)
            else:
                sumCorr += min(corr,0)
        expCorr = sumCorr/numLags
        
    else:
        for i in range(1, numLags):
            corr = calcLaggedCorrelation(s2, s1, i)
      #      print corr
            if (pos == 1):
                sumCorr += max(corr,0)
            else:
                sumCorr += min(corr,0)

    avgCorr = sumCorr/(numLags - 1)

    return avgCorr


# calculate the lead or lag relation between two time series

def calcLeadLagRelation(s1, s2, numLags, pos):
    avgLeadCorr = calcAggregatedCorrelation(s1, s2, numLags, 1, pos)
    avgLagCorr = calcAggregatedCorrelation(s1, s2, numLags, 0, pos)

    if (pos == 1):
        if avgLeadCorr > avgLagCorr:
            return 1, avgLeadCorr
        else:
            return 0, avgLagCorr
    else:
        if avgLeadCorr < avgLagCorr:
            return 1, avgLeadCorr
        else:
            return 0, avgLagCorr

def constructGraph( threshold, numLags, pos ):
    count1 = count2 = 0
    global leadsGraph ,lagsGraph
    leadsGraph,lagsGraph = {},{}
    for key1 in time_series.keys():
        s = time_series[key1]
        
        count1 += 1
        count2 = 0
        dict_Lead = dict_Lag = {}
        
        for key2 in time_series.keys():
            t = time_series[key2]
            
            count2 += 1
            if count1 != count2:
                lead, corr = calcLeadLagRelation(s, t, numLags, pos)
                if (corr > threshold):
                    if (lead == 1):
                        dict_Lead[str(count2)] = corr                        
                    else:
                        dict_Lag[str(count2)] = corr 
                        
        leadsGraph[str(count1)] = dict_Lead
        lagsGraph[str(count1)] = dict_Lag

def leadership_algo(nps_key):
    global time_series
    time_series = defaultdict(list)
    o_f = open("Leadership_{}.csv".format(nps_key),"w")
    input_file = "Subaru_{}_regression.csv".format(nps_key)
    i_f = open( input_file )

    reader = csv.reader( i_f )
    file_lines = []

    for line in reader:

        key = line[0]
        
        values = []

        for value in line[1:len(line)-1]:
            if value == "":
                value = 0
            values.append(float(value))
        
        time_series[key] = values
        
        file_lines.append(line)

    constructGraph(0,5,1)
    l = find_leading(1)
    print l
    o_f.write("Led by {}\n".format(nps_key))
    for item in l:
        line = file_lines[int(item)-1]
        o_f.write("{0},{1}\n".format(line[0],leadsGraph['1'][item]))
    o_f.write("\n"*4)
    o_f.write("Products Leading {}\n".format(nps_key))
    for item in leadsGraph['1'].keys():
        if item not in l :
            line = file_lines[int(item)-1]
            o_f.write("{0},{1}\n".format(line[0],leadsGraph[item]['1']))
    
    o_f.close()
    i_f.close()
    
    
    
def data_output(nps_key):
	
    global finalOutputFileName, finalOutputKeyName
    
    subprocess.call(["C:/Program Files/R/R-2.12.1/bin/R","-f", 'C:/BC/Subaru/AkhileshAutomation/Subaru/r_script_1.R',"--args","Subaru_{}_regression_R_input.csv".format(nps_key),nps_key])
    
    #subprocess.call(["/usr/lib/R/bin/R","-f", '/var/www/pyth/r_script_1.R',"--args","Subaru_{}_regression_R_input.csv".format(nps_key),nps_key])
    
    imp_f = open("Imp.csv")
    corr_f = open("Corr.csv")
    finalOutputFileName = "final_output_{}_regression.csv".format(nps_key)
    finalOutputKeyName = nps_key
    o_f = open(finalOutputFileName,"w")
    s_f = open("Subaru_{}_regression_R_input.csv".format(nps_key))

    reader = csv.reader(s_f)
    header = reader.next()
    s_f.close()

    corr_reader = csv.reader(corr_f)
    imp_reader = csv.reader(imp_f)

    o_f.write("Variable ,%IncMSE ,IncNodePurity ,Correlation value\n")

    for corr_line in corr_reader:
        pass

    list_1 = {}
    i=1
    imp_reader.next()
    for line in imp_reader:
        if line[1] == "NA":
            list_1[0] = [header[i],corr_line[i],line[2],line[1]] 
        else:
            k = float(line[1])
            list_1[k] = [header[i],corr_line[i],line[2],line[1]]                  
        i = i+1
    
    od = collections.OrderedDict(sorted(list_1.items(),reverse = True))  
    for item in od:
        o_f.write("{0},{1},{2},{3}\n".format(od[item][0],od[item][3],od[item][2],od[item][1]))
    
    var_file = open("var_exp.txt".format(nps_key))

    for line in var_file.readlines():
        var_exp = float(line)
    o_f.write("% Var explained : {}\n".format(var_exp))
    var_file.close()
    
    
    o_f.close()
    imp_f.close()
    corr_f.close()
    
    
def get_no_of_points(line):
    i = -1
    p = 0
    prev_val = 0
    prev_count = 0
    for k in line:
        i+=1
        if i == 20:
            break
        if i==0:
            continue
        if k != "":
            if k != prev_val:
                prev_val = k
                prev_count = 1
            else:
                prev_count += 1
            p+=1
    if p == prev_count:
        return 0
    else:
        return p


        
def print_R_input(nps_key):
    o_f = open("Subaru_{}_regression_R_input.csv".format(nps_key),"w")
    i_f = open("Subaru_{}_regression.csv".format(nps_key))

    reader = csv.reader(i_f)

    var = {}
    for line in reader :
        try:

            #skipping blank lines
            if line[18] == "":
                print "amar"
                raise Exception
            #p = line[20]
            #points = get_no_of_points(line)
            
            #print points
            #if points >= 15:

            var[line[0]] = line[1:]
        except Exception:
            continue
    
    data = ""
    for key in var.keys():
        if key.lower() == nps_key.lower():
            data = key + "," + data
        else:
            data = data + key + ","
    data = data[:-1]
    o_f.write(data + "\n")


    # specpial logic for telstra to replace missing values towards the end
    # amar 19 data points for subaru media
    
    
    for i in range(18):
        line = ""
        for key in data.split(","):
            k = var[key][i]
##            if k == "":
##                for j in range(5):
##                    if var[key][i+j+1] != "":
##                        k = var[key][i+j+1]
##                        break
            line = line + k + ","
        o_f.write(line[:-1] + "\n")
    
    
    i_f.close()
    o_f.close()
    data_output(nps_key)
    
    
    
prev_key = ""
ts_dates = []
ts_values = []


date_keys = defaultdict(list)
vals_keys = defaultdict(list)

# for the dependent variables
nps_dates = defaultdict(list)
nps_vals = defaultdict(list)


keys = []


#i_file_name = sys.argv[1]
i_file_name = 'ts_forester_all_data.csv'

#subprocess.call(" python export_to_csv.py "+i_file_name, shell=True)

i_file_name = 'subaru_inupt_data.csv'

i_f = open(i_file_name)

reader = csv.reader(i_f)
header = reader.next()


# Line of the following format4
# level1, level2, level3, level4, level5, measure, date, number, fy, corporate, dependent var
for line in reader:
    #print line
    key = line[0]
    #print key

    dependent = line[6]
    if dependent == "":
        continue
    split_list = []
    key = key.replace("/","_")
    if "d" in str(dependent).lower():
        if "/" in str(dependent).lower():
            split_list = str(dependent).split("/")
        else:
            split_list = [str(dependent)]
        for item in split_list:
            if item not in nps_vals.keys():
                nps_vals[item] = {}
            nps_vals[item][key] = line[7:]
    
    elif "i" in str(dependent).lower():
        if "/" in str(dependent).lower():
            split_list = str(dependent).split("/")
        else:
            split_list = [str(dependent)]
        for item in split_list:
            if item not in vals_keys.keys():
                vals_keys[item] = {}
            vals_keys[item][key] = line[7:]
        
#
for dep_key in nps_vals.keys():
    for nps_key in nps_vals[dep_key].keys():
        print "1"
        output_file = "Subaru_{}_regression.csv".format(nps_key)

        o_f = open( output_file, 'w' )
        write_nps_val = ''

        for val in nps_vals[dep_key][nps_key]:
            write_nps_val = write_nps_val + str(val) + ','
        print "2"
        o_f.write(nps_key + ',' + write_nps_val + os.linesep)
    
        ind_key = "I{}".format(dep_key[1])

        for key in vals_keys[ind_key].keys():
    
            write_val = ''
            for val in vals_keys[ind_key][key]:
                write_val = write_val + str(val) + ","  
            
            o_f.write(key + ',' + write_val + os.linesep)
    
        print "3"
        o_f.close()

        #leadership_algo(nps_key)
        print_R_input(nps_key)

#print nps_key


if(os.path.isfile(finalOutputFileName)):

	print "\n THE FILE EXIST ",finalOutputFileName
	print "\n THE Key EXIST ",finalOutputKeyName 
	subprocess.call(" python persist_random_forest_output.py "+finalOutputFileName+" "+finalOutputKeyName, shell=True)



    
   # print key
   # print date_keys[key]

    

##    if key == prev_key:
##        ts_dates.append(dateFormatted)
##        ts_values.append(line[5])
##    else:
##        ts = Series(ts_dates, ts_values)
##
##        print key
##        print ts
##        
##        telstra[key] = ts
##        prev_key = key
##        ts_dates = []
##        ts_values = []
##        ts_dates.append(dateFormatted)
##        ts_values.append(line[5])
