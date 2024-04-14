from rest_framework.response import Response
from rest_framework.decorators import api_view
from Databases import Kinderneutron
import psycopg2
from .serializers import DetectionSerializer
error_id = 1
elem_id = 1
# Create your views here.
@api_view(['GET','POST'])
def my_data_view(request):
    if request.method =="GET":
        print(request.method)
        raw_data = get_my_data()
        # Convert raw data to a format suitable for serialization
        data = [
            {"id": record[0], "username": record[1], "email": record[2],"auth_token":record[3],"password":"N/A","created_at": record[4],"updated_at": record[5]}
            for record in raw_data
        ]
        
        serializer = DetectionSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        if request.data.get('type') == 'login':
            username = request.data.get('username')
            password = request.data.get('password')
            conn = psycopg2.connect(dbname="kinderneutron_db", user="postgres",  password="123456",  host="psql-db", port="5432")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM public.user WHERE username = '"+username+"' AND password ='"+password+"'")
            records = cursor.fetchall()
            if not records:
                return Response('FAIL',status=400)
            else:
                return Response('SUCESS',status=200)
                
        else:
            elemid  = get_user_id()
            username = request.data.get('username')
            email = request.data.get('email')
            auth_token = request.data.get('auth_token')
            password = request.data.get('password')
            conn = psycopg2.connect(dbname="kinderneutron_db", user="postgres",  password="123456",  host="psql-db", port="5432")
            with conn.cursor() as cursor:
            # The SQL INSERT query
                query = """INSERT INTO "user" (id, username, email,password,auth_token) VALUES (%s, %s,%s,%s,%s)"""
            
            # Data to insert
                data = (elemid,username,email,password,auth_token)
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
    cursor.execute("SELECT id, username,email,auth_token,created_at,updated_at FROM public.user")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

def get_user_id():
    conn = psycopg2.connect(dbname="kinderneutron_db", user="postgres",  password="123456",  host="psql-db", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM public.user")
    records = cursor.fetchone()  
    (records,) = records
    if records == 0:
        return "USER-01"
    else:
        cursor.execute("SELECT id FROM public.user ORDER BY created_at DESC LIMIT 1")
        records = cursor.fetchone()
        (records,) = records
        return "USER-0"+str(int(records[len("DET-0"):])+1)
   