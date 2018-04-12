import mysql.connector as db

db_con = -1
crs = -1

def createDB():
    db_connection = db.connect(host='10.1.141.234', port=3306, user='oskar', password='', database='oskar')
    cursor = db_connection.cursor()
    cursor.execute("DROP TABLE userData")
    cursor.execute("CREATE TABLE IF NOT EXISTS userData(userName TEXT, gender INT, age INT")
    db_con = db_connection
    crs = cursor
    return cursor, db_connection

def addToDB(userName, gender, age):
    add = ("INSERT INTO userData "
               "(userName, gender, age) "
               "VALUES (%s, %s, %s)")
    data = (userName, gender, age)
    crs.execute(add, data)
    db_con.commit()


createDB()
addToDB('Lena', 1, 112)
crs.execute("SELECT * from userData")
print crs.fetchall()