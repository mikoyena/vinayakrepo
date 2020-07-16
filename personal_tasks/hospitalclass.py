# hospital class
# functionality to add the medical speciality without deleting the existing medical speciality.

class Hospitals:
    num_min_beds = 15
    def __init__(self, name, num_of_doctors , num_of_nurses, medical_speciality):
        self.name = name
        self.num_of_doctors = num_of_doctors
        self.num_of_nurses = num_of_nurses
        self.medical_speciality = medical_speciality

    def details(self):
        print(f'Hospital name: {self.name}')
        print(f'Number of Doctors: {self.num_of_doctors}')
        print(f'Number of Nurses: {self.num_of_nurses}')
        print(f'Medical Speciality:{self.medical_speciality}')
        print(f'Number of Beds:{self.num_min_beds}\n')

    def modify_med_spec(self,lst):
        for val in lst:
            tmplist = self.medical_speciality
            tmplist.append(val)

    @classmethod
    def modify_min_num_beds(cls, value):
        cls.num_min_beds = value


hospital_A = Hospitals("Health Care PVT LTD", 66, 156,["A","B"])
hospital_A.details()
hospital_A.modify_med_spec(["Hi","vinayak","abc"])


Hospitals.modify_min_num_beds(20)
hospital_B = Hospitals("criticare PVT LTD", 56, 196,["b"])
hospital_B.details()


hospital_C = Hospitals("Heidelberg Health care PVT LTD", 86, 194,["c"])
hospital_C.details()


hospital_A.details()
