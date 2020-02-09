from kafka import KafkaConsumer
import json
import pymongo

mongoclient = pymongo.MongoClient('localhost', 27017)
mongo_db = mongoclient['Data_Eng_Petrol_Data']
collection_name = 'Station_data'
mongocollection = mongo_db[collection_name]
mongocollection.delete_many({})

consumer = KafkaConsumer("topic4vinayak", bootstrap_servers=['localhost:9092'], group_id=None,
                         auto_offset_reset='earliest', consumer_timeout_ms=5000
                                     , enable_auto_commit = True)
try:
    for msg in consumer:
        decoded_msg = msg.value
        decoded_msgtmp = decoded_msg.decode("utf-8")
        strval = json.loads(decoded_msgtmp)
        finaldict = strval['stations']
        for line in finaldict:
            mongocollection.insert_one(line)

except Exception as e:  

    print(e)





