from rest_framework.response import Response
from rest_framework.decorators import api_view
from Databases import Kinderneutron
import psycopg2
from .serializers import DetectionSerializer
# Create your views here.
@api_view(['GET','POST'])
def my_data_view(request):
    raw_data = get_my_data()
    # Convert raw data to a format suitable for serialization
    data = [
        {"id": record[0], "timestamp": record[1], "result": record[2],"created_at": record[3],"updated_at": record[4]}
        for record in raw_data
    ]
    
    serializer = DetectionSerializer(data, many=True)
    return Response(serializer.data)


def get_my_data():
    # Assuming you've already configured your database settings
    conn = Kinderneutron.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, result,created_at,updated_at FROM detection")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records
