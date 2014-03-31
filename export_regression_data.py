import csv, MySQLdb, sys
from collections import defaultdict


try:
	mydb = MySQLdb.connect(host='localhost', user='root', passwd='amar310884', db='subaru')
	#cursor = mydb.cursor()
	cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
except Exception:
	print "\n Database is not connected"
	exit();	
	
inputCsvFileName = "subaru_inupt_data.csv"

cursor.execute('select * from regressions ')
regressionsRows = cursor.fetchone ()

if len(regressionsRows) ==0:
	print "\n No data available..."
	exit()


'''print mydict.keys()[mydict.values().index(16)] # Prints george
print list(mydict.keys())[list(mydict.values()).index(16)] # Prints george
'''
#Dependented Data
cursor.execute('select distinct `date` from '+regressionsRows['d_var_table_name']+' where `date` BETWEEN "'+str(regressionsRows["start_date"])+'" AND "'+str(regressionsRows["end_date"])+'" order by `date` ')
weeklyDates = cursor.fetchall ()
dictWeekDates = {}

#Add coloumns header 
for index, row in enumerate(weeklyDates) :
	dictWeekDates[index+1] =  row['date']
	

sqlDependent = 'SELECT * FROM '+regressionsRows['d_var_table_name']+' WHERE `unique_id` = "'+regressionsRows['d_var_unique_id']+'" AND `date` BETWEEN "'+str(regressionsRows["start_date"])+'" AND "'+str(regressionsRows["end_date"])+'" ORDER BY `unique_id` , `date` '

print sqlDependent
cursor.execute(sqlDependent)
data = cursor.fetchall()

valuesStartingColumn  = 6
dictDepData = defaultdict(dict)
	

for index, row in enumerate(data) :
	
	#print "\n",index
	#exit()
	
	#indexOfUniqId  = dictUniqueIdList.keys()[dictUniqueIdList.values().index(row['unique_id'])]
	indexOfUniqId  = row['unique_id']
	
	dictDepData[indexOfUniqId][0] = row['unique_id']
	dictDepData[indexOfUniqId][1] = ''
	dictDepData[indexOfUniqId][2] = row['unique_id']
	dictDepData[indexOfUniqId][3] = row['unique_id']
	dictDepData[indexOfUniqId][4] = row['unique_id']
	dictDepData[indexOfUniqId][5] = '0.5'
	dictDepData[indexOfUniqId][6] = 'D1'


	dateColumnNo =  dictWeekDates.keys()[dictWeekDates.values().index(row['date'])]

	dictDepData[indexOfUniqId][int(dateColumnNo+valuesStartingColumn)] = row['value']
			
# Insert value of "Dependent" = 'D1' for first record 		 
#dictDepData[1][6] = 'D1'

#Independent data

cursor.execute('select distinct `date` from '+regressionsRows['i_var_table_name']+' where `date` BETWEEN "'+str(regressionsRows["start_date"])+'" AND "'+str(regressionsRows["end_date"])+'" order by `date` ')
weeklyDates = cursor.fetchall ()
dictWeekDates = {}

#Add coloumns header 
for index, row in enumerate(weeklyDates) :
	dictWeekDates[index+1] =  row['date']
	


sqlIndependent ='SELECT * FROM '+regressionsRows['i_var_table_name']+' WHERE '

if regressionsRows['i_var_unique_id'] != 'ALL':
	sqlIndependent += '`unique_id` = "'+regressionsRows['i_var_unique_id']+'" AND '
	
sqlIndependent += ' `date` BETWEEN "'+str(regressionsRows["start_date"])+'" AND "'+str(regressionsRows["end_date"])+'" ORDER BY `unique_id` , `date` '
	
print sqlIndependent
cursor.execute(sqlIndependent)
data = cursor.fetchall()

valuesStartingColumn  = 6
dictIndpendentData = defaultdict(dict)
	

for index, row in enumerate(data) :
	
	#print "\n",index
	#exit()
	
	#indexOfUniqId  = dictUniqueIdList.keys()[dictUniqueIdList.values().index(row['unique_id'])]
	indexOfUniqId  = row['unique_id']
	
	dictIndpendentData[indexOfUniqId][0] = row['unique_id']
	dictIndpendentData[indexOfUniqId][1] = ''
	dictIndpendentData[indexOfUniqId][2] = row['unique_id']
	dictIndpendentData[indexOfUniqId][3] = row['unique_id']
	dictIndpendentData[indexOfUniqId][4] = row['unique_id']
	dictIndpendentData[indexOfUniqId][5] = '0.5'
	dictIndpendentData[indexOfUniqId][6] = 'I1'


	dateColumnNo =  dictWeekDates.keys()[dictWeekDates.values().index(row['date'])]

	dictIndpendentData[indexOfUniqId][int(dateColumnNo+valuesStartingColumn)] = row['value']
	
	
headerTop = ['uniqueid', 'forecasting','tool tip','node name','Category','delta','Dependent','10-Aug','Weekly']
writer = csv.writer(open(inputCsvFileName, 'wb'))

writer.writerow(headerTop)	

for key, value in dictDepData.items():
   writer.writerow( value.values())	
   	
for key, value in dictIndpendentData.items():
   writer.writerow( value.values())		
		
print "\n Done"		


