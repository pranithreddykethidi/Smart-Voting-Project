import pymysql

def connect():
    con=pymysql.connect(host="localhost",user="root",password="root",database="smart_voting",charset="utf8")
    return con
