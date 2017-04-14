import mysql.connector
from mysql.connector import Error

def connect():
        """ Connect to MySQL DB """
        try:
                conn = mysql.connector.connect(host="43.229.84.119",
                                                   database="ballerle_CS",
                                                   user="ballerle_csusr",
                                                   password="%;@TSMHHP9v]")

                if conn.is_connected():
                        print("Connected to MySQL Database")

                return conn


        except Error as e:
                print(e)


conn = connect()
cursor = conn.cursor()

def insert_new_device_status(mac_addr, timestmp, status, location):
        """ Insert device status """
        query = "INSERT INTO TBL_HISTORY(MAC_ADDRESS, HISTORY_DATETIME, STATUS, LOCATION_ID) " \
                        "VALUES(%s, %s, %s, %s)"
        args = (mac_addr, timestmp, status, location)
        cursor.execute(query, args)

insert_new_device_status("D8:C4:E9:78:09:B4", "2017-01-02 11:30:01", "out", "1")
insert_new_device_status("00:1D:D9:F9:79:43", "2017-01-02 11:35:25", "out", "1")

cursor.execute("select * from TBL_HISTORY")
rows = cursor.fetchall()
print('Total Rows: ', cursor.rowcount)
for row in rows:
        print(row)

conn.close()
