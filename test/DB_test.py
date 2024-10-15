import requests
import pprint
import smartsheet
import psycopg2

db = psycopg2.connect(host='localhost', dbname='Smartsheet',user='openpg',password='openpngpwd',port=5432)

def execute(self,query,args={}):
    self.cursor.execute(query,args)
    row = self.cursor.fetchall()
    return row


def insertDB(schema,table,colum,data):
    cursor = db.cursor()
    sql = " INSERT INTO {schema}.{table}({colum}) VALUES ('{data}');".format(schema=schema,table=table,colum=colum,data=data)
    try:
        print(sql)
        cursor.execute(sql)
        db.commit()
    except Exception as e :
        print(" insert DB err ",e) 
    
def readDB(schema,table,colum):
    cursor = db.cursor()
    sql = " SELECT {colum} from {schema}.{table}".format(colum=colum,schema=schema,table=table)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result )
    except Exception as e :
        result = (" read DB err",e)
    
    return result

def updateDB(schema,table,colum,value,condition):
    cursor = db.cursor()
    sql = " UPDATE {schema}.{table} SET {colum}='{value}' WHERE {colum}='{condition}' ".format(schema=schema
    , table=table , colum=colum ,value=value,condition=condition )
    try :
        cursor.execute(sql)
        db.commit()
    except Exception as e :
        print(" update DB err",e)

def deleteDB(schema,table,condition):
    cursor = db.cursor()
    sql = " delete from {schema}.{table} where {condition} ; ".format(schema=schema,table=table,condition=condition)
    try :
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print( "delete DB err", e)

readDB("public","Smartsheet","*")