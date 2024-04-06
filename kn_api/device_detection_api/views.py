from rest_framework.response import Response
from rest_framework.decorators import api_view
from Databases import Kinderneutron
import psycopg2
from .serializers import DeviceSerializer
# Create your views here.
@api_view(['GET','POST'])
def my_data_view(request):
    raw_data = get_my_data()
    # Convert raw data to a format suitable for serialization
    data = [
        {"id": record[0], "username": record[1], "device_name": record[2],"login_time": record[3],"updated_at": record[4]}
        for record in raw_data
    ]
    
    serializer = DeviceSerializer(data, many=True)
    return Response(serializer.data)


def get_my_data():
    # Assuming you've already configured your database settings
    conn = Kinderneutron.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, device_name,login_time,updated_at FROM device")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records