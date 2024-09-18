from kafka import KafkaConsumer
import mysql.connector
import json
import os

from dotenv import load_dotenv
load_dotenv()

# Connect to MySQL
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password=os.getenv('MYSQL_PASSWORD'),
    database='real_estate'
)
cursor = db_connection.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS properties (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        location VARCHAR(255),
        bedrooms VARCHAR(50),
        bathrooms VARCHAR(50),
        size VARCHAR(50),
        date VARCHAR(50),
        amenities TEXT,
        url TEXT,
        property_type VARCHAR(50),
        payment_type VARCHAR(50),
        price VARCHAR(50)
    )
''')

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    'property_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='property-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Consume messages
for message in consumer:
    property_data = message.value
    cursor.execute('''
        INSERT INTO properties (title, location, bedrooms, bathrooms, size, date, amenities, url, property_type, payment_type, price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        property_data['Title'], property_data['Location'], property_data['Bedrooms'], property_data['Bathrooms'],
        property_data['Size'], property_data['Date'], ', '.join(property_data['Amenities']),
        property_data['Url'], property_data['Property Type'], property_data['Payment_type'], property_data['Price']
    ))
    db_connection.commit()
