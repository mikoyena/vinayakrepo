from matplotlib import pyplot as plt
import pymongo
from collections import Counter


dlist =[]
mongoclient = pymongo.MongoClient('localhost', 27017)
mongo_db = mongoclient['Data_Eng_Petrol_Data']
collection_name = 'Station_data'
mongocollection = mongo_db[collection_name]

try:
	mydoc = mongocollection.find()
except Exception as e:
	print(e)

for doc in mydoc:
	dlist.append(doc['place'])

converted_list = [x.upper() for x in dlist]

c = Counter(converted_list)

cities = list(c.keys())
fuelpumpfreq = list(c.values())

plt.bar(cities,fuelpumpfreq,label ='Bars') 
plt.xlabel('X-axis')
plt.ylabel('Y-axis')    
plt.title('Frequencey of petrol pumps')
plt.legend()
plt.show()

