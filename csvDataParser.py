#!/usr/bin/python

import csv, MySQLdb, traceback
from collections import defaultdict



#i_file_name = sys.argv[1]
i_file_name = 'C:\BC\Subaru\AkhileshAutomation\Subaru\SubaruImpressions.csv'

if i_file_name.find('SubaruSpend.csv') > 0:
	tableName = "spend"
elif i_file_name.find('SubaruImpressions.csv') > 0:
	tableName = "impressions"
else:
	print "\n File name is not correct..."
	exit()


try:
	i_f = open(i_file_name)
except Exception:
	print "Error: can\'t find file or read data ",i_file_name
	exit();

if i_f:
	
	reader = csv.reader(i_f)
	if(reader):
		try:
			mydb = MySQLdb.connect(host='localhost', user='root', passwd='amar310884', db='Subaru')
			cursor = mydb.cursor()
		except Exception:
			print "\n Database is not connected"
			exit();	
			
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

	#print header

	num_weeks = len(header) - 4
	weeks = header[4:num_weeks]

	prev_line_2 = ""
	prev_line_1 = ""


	weekly_values = defaultdict(list)
	monthly_values = defaultdict(list)

	for index, line in enumerate(reader):

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
		#if(index==9):
		#	print key," LOLOLOOLO", index

		
		# Once the key is constructed, we need to store the time series values
		# We have weekly numbers, we store both weekly and monthly numbers
		# in two data structures
		# Store the weekly time series
		
		for i in range(4,num_weeks):
			
			if line[i] == "":
				weekly_values = 0.0
			else:
				weekly_values = str(line[i])
			
			#print " \n ",weeks[i-4], " : ",line[i]
				
			#print "\n ",'INSERT INTO  impressions(unique_id,date,value,type) VALUES("'+key+'",STR_TO_DATE("'+weeks[i-4]+'", \'%d/%m/%Y\'),"'+str(weekly_values)+'","weekly" )'
			#exit();
			try:
				cursor.execute('INSERT INTO  '+tableName+'(unique_id,date,value,type) VALUES("'+key+'",STR_TO_DATE("'+weeks[i-4]+'", \'%d/%m/%Y\'),"'+str(weekly_values)+'","weekly" )')
			except MySQLdb.Warning, e:
				print "\n ", e[0], e.args[1]
				exit();	
			except:
				print "\n Something is wrong..."
				exit();	
				
	mydb.commit()
	cursor.close()
	print "Done"
				
				       
