import requests 
from confluent_kafka import Producer
import time
import json

topic = "topic_moviedb_details"
kafka_config = {
    "bootstrap.servers": "localhost:9092",  # Change this to your Kafka server address
}

producer = Producer(kafka_config)

counter = 3
while True:
    url = f"https://api.themoviedb.org/3/movie/{counter}?api_key=******fe76b80ebd8dfa5158f8dc108a7"
    headers = {
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    counter += 1
    if response.status_code == 200:
        data = json.dumps(response.json())
        producer.produce(topic, key="moviedb", value=data)
        time.sleep(10)
        producer.flush()
        print(response.json())
    else:
        print(response.status_code)
    
   


    
    # scala version: 2.12.15
    # spark version: 3.2.4
    # elasticsearch-spark-30_2.12
    # elasticsearch: 8.2


