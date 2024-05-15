import psycopg2
import json
import datetime
import os 
class Database_Update:
    def __init__(self):
        conn = psycopg2.connect(dbname="kinderneutron_db", user="postgres",  password="123456",  host="psql-db", port="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM detection")
        records = cursor.fetchone()  
        if records[0] == 0:
            self.detection_id = 1
        else:
            cursor.execute("SELECT id FROM detection ORDER BY created_at DESC LIMIT 1")
            records = cursor.fetchone()
            (records,) = records
            self.detection_id = int(records[len("DET-0"):])+1
        self.error_id = 1
        
    def dbupdate(self):
        filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data.json'))
        person_detection_status = ''
        with open(filepath, 'r+') as file:
                data = json.load(file)
                person_detection_status = data['person_detected'] 
        if person_detection_status =='yes':
            self.detection_id = self.detection_id+1
            data_val = ('DET-0'+str(self.detection_id),datetime.datetime.now(),'Deteted' )
            conn = psycopg2.connect(dbname="kinderneutron_db", user="postgres",  password="123456",  host="psql-db", port="5432")
            with conn.cursor() as cursor:
        # The SQL INSERT query
                query = """INSERT INTO "detection" (id, timestamp, result) VALUES (%s, %s,%s)"""
            
            # Data to insert
                
                
            # Execute the query
                cursor.execute(query, data_val)
                # print(data)
            # Commit the transaction
                try:
                    conn.commit()
                    
                except Exception as e:
                    query1 = """INSERT INTO "error_log" (id, userid, error_type,message,created_at,updated_at) VALUES (%s, %s,%s,%s)"""
                    data = ("DBERROR-0"+str(self.error_id),"N/A","Database Error","Error Due to Invalid Post Request")
                    cursor.execute(query1, data)
                    self.error_id = self.error_id+1
        else:
            self.detection_id = self.detection_id+1
            data_val = ('DET-0'+str(self.detection_id),datetime.datetime.now(),'Not Deteted' )
            conn = psycopg2.connect(dbname="kinderneutron_db", user="postgres",  password="123456",  host="psql-db", port="5432")
            with conn.cursor() as cursor:
        # The SQL INSERT query
                query = """INSERT INTO "detection" (id, timestamp, result) VALUES (%s, %s,%s)"""
            
            # Data to insert
                
                
            # Execute the query
                cursor.execute(query, data_val)
                # print(data)
            # Commit the transaction
                try:
                    conn.commit()
                    
                except Exception as e:
                    query1 = """INSERT INTO "error_log" (id, userid, error_type,message,created_at,updated_at) VALUES (%s, %s,%s,%s)"""
                    data = ("DBERROR-0"+str(self.error_id),"N/A","Database Error","Error Due to Invalid Post Request")
                    cursor.execute(query1, data)
                    self.error_id = self.error_id+1
