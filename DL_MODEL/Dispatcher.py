import pika
from neo4j import GraphDatabase
import serial
import json

# Neo4j credentials and connection
uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"
driver = GraphDatabase.driver(uri, auth=(username, password))

# RabbitMQ connection parameters
rabbitmq_host = 'localhost'
queue_name = 'arduino_commands'

# Arduino serial connection
arduino_port = '/dev/ttyACM0'
arduino_baudrate = 9600
ser = serial.Serial(arduino_port, arduino_baudrate)

def fetch_pin(message):
    with driver.session() as session:
        query = (
            "MATCH (camera:Camera)-[:HAS_A_AREA]->(area:Area)-[:CONNECTED_TO]->(bulb:Bulb) "
            "WHERE area.name = $area_name "
            "RETURN bulb.pin AS pin"
        )
        result = session.run(query, area_name=message)
        record = result.single()
        if record:
            return record['pin']
        else:
            return None

def callback(ch, method, properties, body):
    message = body.decode('utf-8')
    print(f"Received message: {message}")
    
    pin = fetch_pin(message)
    if pin is not None:
        print(f"Sending pin {pin} to Arduino")
        ser.write(bytes(str(pin), 'utf-8'))
    else:
        print("Area not found or pin not assigned.")

def consume_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(f"Waiting for messages from {queue_name}. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    consume_messages()
