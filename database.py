import mysql.connector as db
import itertools


def connectToDB():
    db_connection = db.connect(host='10.1.141.234', port=3306, user='oskar', password='', database='oskar')
    cursor = db_connection.cursor(buffered=True)  
    #cursor.execute("DROP TABLE userData")
    cursor.execute("CREATE TABLE IF NOT EXISTS userData(userName TEXT, uniqueID TEXT, gender TEXT, age TEXT, shoeSize TEXT, clothSize TEXT)")
    return cursor, db_connection

def addToDB(userName, uniqueID, gender, age, shoeSize, clothSize):
    crs, db_con = connectToDB()

    crs.execute("SELECT uniqueID, COUNT(*) FROM userData WHERE uniqueID = " + str(uniqueID) + " GROUP BY uniqueID")
    list_of_ids = list(itertools.chain.from_iterable(crs))
    print(list_of_ids)
    if len(list_of_ids) != 0:
        print ('user already exists')
        return
    sql = "insert into userData VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % \
       (userName, uniqueID, gender, age, shoeSize, clothSize)
    print ('add new user to database with data (userName, uniqueID, gender, age, shoeSize, clothSize) = ' ,userName, uniqueID, gender, age, shoeSize, clothSize)
    crs.execute(sql)
    db_con.commit()
    crs.close()
    db_con.close()

def getFullContent():
    crs, db_con = connectToDB()
    query = "SELECT * from userData"
    crs.execute(query)
    fetchAll = str(crs.fetchall())
    crs.close()
    db_con.close()
    return fetchAll

def getUserContent(uniqueID):
    crs, db_con = connectToDB()
    query = "SELECT * from userData WHERE uniqueID = " + str(uniqueID)
    crs.execute(query)
    fetchUser = str(crs.fetchall())
    crs.close()
    db_con.close()
    return fetchUser    

addToDB('Lena','123456', 'F', '112', '38', 'S')
addToDB('Lena','123477', 'F', '112', '38', 'S')
print ('---------')
print (getFullContent())
print ('---------')
print (getUserContent('123456'))