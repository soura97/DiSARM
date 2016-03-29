import sys
import cx_Oracle

def printf (format,*args):
	sys.stdout.write (format % args)

def printException (exception):
	error, = exception.args
	printf ("Error code = %s\n",error.code);
	printf ("Error message = %s\n",error.message);

username = 'u1'
password = 'pwd1'
databaseName = "DISARM"

try:
	connection = cx_Oracle.connect (username,password,databaseName)
except cx_Oracle.DatabaseError, exception:
	printf ('Failed to connect to %s\n',databaseName)
	printException (exception)
	exit (1)

cursor = connection.cursor ()

sql = """CREATE TABLE DISARM (
         CATEGORY INT,
         FILE_NAME CHAR(8),
         SUMMARY CHAR(50) )"""

cursor.execute(sql)
with open(thefile, "r") as output:
	lines=output.readlines()

cursor.execute ("""INSERT INTO DISARM (CATEGORY,FILE_NAME,SUMMARY) VALUES(%d, %s, %s)""",(str(i),outname,lines))

cursor.close()
connection.close()


