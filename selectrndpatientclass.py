import random
import datetime

class citycouncil:
	batch_size = 5
	def __init__(self , city , patientlist):
		self.city = city
		self.patientlist = patientlist

	@classmethod
	def modify_batch_size(cls, value):
		cls.batch_size = value

	def splitpatients(self):
		for i in range(0,len(self.patientlist),self.batch_size):
			yield self.patientlist[i:i+self.batch_size]

	def showpatient(self , res):
		print("results for city: " +self.city)
		print('test began!')
		for item in res:
				random_num = random.randint(0, self.batch_size - 1)
				dt = datetime.datetime.now()
				print(f'Patient {item[random_num]} was tested on datetime {dt}')
		print('test completed!\n')



city1 = citycouncil("heidelberg", ['p1','p2','p3','p4','p5','p6','p7','p8','p9','p10','p11','p12','p13','p14','p15','p16','p17','p18','p19','p20'])

result = city1.splitpatients()

city1.showpatient(result)



city2 = citycouncil("mannheim", ['p1','p2','p3','p4','p5','p6','p7','p8','p9','p10','p11','p12','p13','p14','p15','p16','p17','p18','p19','p20'])

citycouncil.modify_batch_size(4)
result = city2.splitpatients()
city2.showpatient(result)
