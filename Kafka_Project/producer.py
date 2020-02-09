from kafka import KafkaClient, KafkaProducer, KafkaConsumer
import csv
import json
import requests

client = KafkaClient("localhost:9092")
producer = KafkaProducer(bootstrap_servers='localhost:9092')

try:
    with open("geodetails.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            tmplat = row[0]
            tmplng = row[1]
            parameters = {
            "lat": tmplat,
            "lng": tmplng,
            "rad": 3,
            "sort": "dist",
            "type": "all",
            "apikey": "00000000-0000-0000-0000-000000000002"
            }
            response = requests.get("https://creativecommons.tankerkoenig.de/json/list.php", params=parameters)
            tmpval = response.text.title()
            finrsp = bytes(tmpval,encoding="utf-8")
            print(finrsp)
            producer.send('topicvinayak',value=finrsp)

except Exception as e:
    print(e)



