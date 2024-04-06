from rest_framework.response import Response
from rest_framework.decorators import api_view
from Databases import Kinderneutron
import psycopg2
from .serializers import ErrorLogSerializer
# Create your views here.
@api_view(['GET','POST'])
def my_data_view(request):
    raw_data = get_my_data()
    # Convert raw data to a format suitable for serialization
    data = [
        {"id": record[0], "user_id": record[1], "error_type": record[2],"message": record[3],"created_at": record[4],"updated_at": record[5]}
        for record in raw_data
    ]
    
    serializer = ErrorLogSerializer(data, many=True)
    return Response(serializer.data)


def get_my_data():
    # Assuming you've already configured your database settings
    conn = Kinderneutron.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, error_type,message,created_at,updated_at FROM error_log")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records
