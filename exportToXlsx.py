import xlsxwriter, MySQLdb
from collections import defaultdict

try:
	mydb = MySQLdb.connect(host='localhost', user='root', passwd='amar310884', db='Subaru')
	cursor = mydb.cursor()
except Exception:
	print "\n Database is not connected"
	exit();	
	
tableName = "impressions"

cursor.execute('select distinct `date` from '+tableName+' order by `date` ')

weeklyDates = cursor.fetchall ()
dictWeekDates = {}

'''print mydict.keys()[mydict.values().index(16)] # Prints george
print list(mydict.keys())[list(mydict.values()).index(16)] # Prints george
'''

if len(weeklyDates) ==0:
	print "\n No data available..."
	exit()

# file name
workbook = xlsxwriter.Workbook('C:\BC\Subaru\AkhileshAutomation\Subaru\Subaruimpression_import.xlsx')
worksheet = workbook.add_worksheet('spend') #sheet name
#Add Unique-id coloumns header 
worksheet.write(1,0, 'Unique-id')
#Add weeks coloumns header 
for index, row in enumerate(weeklyDates) :
	worksheet.write(1,index+1, str(row[0]))
	dictWeekDates[index+1] =  row[0]

#fetch distinct unique-ids
cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
#sql = 'SELECT DISTINCT `unique_id` FROM '+tableName+' limit 0,50'
sql = 'SELECT * FROM '+tableName
cursor.execute(sql)
data = cursor.fetchall()
uniqueIdList = []
inc = 1
for index, row in enumerate(data) :
	if(row['unique_id'] in uniqueIdList):
		
		dateColumnNo =  dictWeekDates.keys()[dictWeekDates.values().index(row['date'])]
		#Write weekly value
		worksheet.write(inc,dateColumnNo, row['value'])
		
		
	else:
		
		#Add unique-id data
		worksheet.write(inc+1,0, str(row['unique_id']))
		dateColumnNo =  dictWeekDates.keys()[dictWeekDates.values().index(row['date'])]
		#Write weekly value
		worksheet.write(inc+1,dateColumnNo, row['value'])
		uniqueIdList.append( str(row['unique_id']))
		inc +=1

workbook.close()

print "\n", len(uniqueIdList)
