import psycopg2
class Kinderneutron:
    def __init__(self):
        self.dbname="kinderneutron_db" 
        self.user="postgres"
        self.password="123456"
        self.host="psql-db"
        self.port="5432"
    
    def connect_db():
        conn = psycopg2.connect(dbname="kinderneutron_db", user="postgres",  password="123456",  host="psql-db", port="5432")
        return conn