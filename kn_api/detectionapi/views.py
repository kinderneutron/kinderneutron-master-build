from rest_framework.response import Response
from rest_framework.decorators import api_view
from Databases import Kinderneutron
import psycopg2
from .serializers import DetectionSerializer
error_id = 1
# Create your views here.
@api_view(['GET','POST'])
def my_data_view(request):
    if request.method =="GET":
        print(request.method)
        raw_data = get_my_data()
        # Convert raw data to a format suitable for serialization
        data = [
            {"id": record[0], "timestamp": record[1], "result": record[2],"created_at": record[3],"updated_at": record[4]}
            for record in raw_data
        ]
        
        serializer = DetectionSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        elemid = request.data.get('id')
        timestamp = request.data.get('timestamp')
        result = request.data.get('result')
        conn = psycopg2.connect(dbname="kinderneutron_db", user="postgres",  password="123456",  host="psql-db", port="5432")
        with conn.cursor() as cursor:
        # The SQL INSERT query
            query = """INSERT INTO "detection" (id, timestamp, result) VALUES (%s, %s,%s)"""
        
        # Data to insert
            data = (elemid,timestamp,result)
            print(data)
        # Execute the query
            cursor.execute(query, data)
        
        # Commit the transaction
            try:
                conn.commit()
                
            except Exception as e:
                query1 = """INSERT INTO "error_log" (id, userid, error_type,message,created_at,updated_at) VALUES (%s, %s,%s,%s)"""
                data = ("DBERROR-0"+str(error_id),"N/A","Database Error","Error Due to Invalid Post Request")
                cursor.execute(query1, data)
                error_id = error_id+1
        return Response('Sucess')
    else:
        return Response('Failed Request')

def get_my_data():
    # Assuming you've already configured your database settings
    conn = Kinderneutron.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, result,created_at,updated_at FROM detection")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records
