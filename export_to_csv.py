import csv, MySQLdb, sys
from collections import defaultdict

try:
	inputCsvFileName = sys.argv[1]
except Exception:
	print "\n Please give name of csv input file..."
	exit();	
	

try:
	mydb = MySQLdb.connect(host='localhost', user='root', passwd='123', db='media')
	cursor = mydb.cursor()
except Exception:
	print "\n Database is not connected"
	exit();	
	
tableName = "impressions"
 

cursor.execute('select distinct `date` from '+tableName+' order by `date` ')
weeklyDates = cursor.fetchall ()

cursor.execute('select distinct `unique_id` from '+tableName)
uniqueIdList = cursor.fetchall ()

dictWeekDates = {}
dictUniqueIdList = {}

'''print mydict.keys()[mydict.values().index(16)] # Prints george
print list(mydict.keys())[list(mydict.values()).index(16)] # Prints george
'''

if len(weeklyDates) ==0:
	print "\n No data available..."
	exit()


#Add coloumns header 
for index, row in enumerate(weeklyDates) :
	dictWeekDates[index+1] =  row[0]
	
for index, row in enumerate(uniqueIdList) :
	dictUniqueIdList[index+1] =  str(row[0])
	


#fetch distinct unique-ids
cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
#sql = 'SELECT DISTINCT `unique_id` FROM '+tableName+' limit 0,50'
sql = 'SELECT * FROM '+tableName
cursor.execute(sql)
data = cursor.fetchall()

valuesStartingColumn  = 6
dictAllData = defaultdict(dict)
	

for index, row in enumerate(data) :
	#print "\n",index
	#exit()
	indexOfUniqId  = dictUniqueIdList.keys()[dictUniqueIdList.values().index(row['unique_id'])]

	dictAllData[indexOfUniqId][0] = row['unique_id']
	dictAllData[indexOfUniqId][1] = ''
	dictAllData[indexOfUniqId][2] = row['unique_id']
	dictAllData[indexOfUniqId][3] = row['unique_id']
	dictAllData[indexOfUniqId][4] = row['unique_id']
	dictAllData[indexOfUniqId][5] = '0.5'
	dictAllData[indexOfUniqId][6] = 'I1'


	dateColumnNo =  dictWeekDates.keys()[dictWeekDates.values().index(row['date'])]

	dictAllData[indexOfUniqId][int(dateColumnNo+valuesStartingColumn)] = row['value']
			
# Insert value of "Dependent" = 'D1' for first record 		 
dictAllData[1][6] = 'D1'


headerTop = ['uniqueid', 'forecasting','tool tip','node name','Category','delta','Dependent','10-Aug','Weekly']
writer = csv.writer(open(inputCsvFileName, 'wb'))

writer.writerow(headerTop)		
for key, value in dictAllData.items():
   writer.writerow( value.values())		
		
print "\n Done"		

