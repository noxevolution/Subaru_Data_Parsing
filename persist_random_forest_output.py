#!/usr/bin/python

import csv, MySQLdb, traceback, sys
from collections import defaultdict


try:
	i_file_name = sys.argv[1]
	finalOutputKeyName = sys.argv[2]
except Exception:
	print "\n Please give name of csv input file..."
	exit();	

#i_file_name = 'final_output_Brand_Brisbane_BTQ-7_Brisbane_regression1.csv'
#finalOutputKeyName = 'Brand_Brisbane_BTQ-7_Brisbane'

try:
	i_f = open(i_file_name,'r')
except Exception:
	print "Error: can\'t find file or read data ",i_file_name
	exit();

if i_f:
	
	totalLines1 =  len(i_f.readlines())
	totalLines = totalLines1 - 2
	i_f.seek(0)
	reader = csv.reader(i_f)
	 	
	if(reader):
		try:
			mydb = MySQLdb.connect(host='localhost', user='root', passwd='amar310884', db='subaru')
			cursor = mydb.cursor()
		except Exception:
			print "\n Database is not connected"
			exit();	
			
	dump = reader.next()
	
	for index, line in enumerate(reader):
		
		if ( index > totalLines):
			break
		elif( index == totalLines):
			try:
			
				lstr = line[0].split(':')
								
				cursor.execute('INSERT INTO  random_forest_variance_explained  (dependent_variable,independent_variable,model_variance) VALUES("D1","'+finalOutputKeyName+'","'+lstr[1]+'")')
			
			except Exception:
			
				print "\n Something is wrong while inserting into table random_forest_variance_explained..."
				
		elif( index < totalLines):		
			
			#print "\n ",'INSERT INTO  '+tableName+'(unique_id, 	inc_mse,inc_node_purity,correlation) VALUES("'+line[0]+'","'+line[1]+'","'+line[2]+'","'+line[3]+'")'
			#exit();
			
			try:
			
				cursor.execute('INSERT INTO  random_forest_output (unique_id,inc_mse,inc_node_purity,correlation) VALUES("'+line[0]+'","'+line[1]+'","'+line[2]+'","'+line[3]+'")')
			
			except Exception:
				print "\n Something is wrong..."
				#exit();	
			
					
	mydb.commit()
	cursor.close()
	print "Done"
				
				       
