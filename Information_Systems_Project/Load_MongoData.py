import pandas as pd
import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

# connecting to desired database

db = client["WasteManagement"]

# connecting to a collection, where our data will be stored.
collectionCity = db["Cities"]
collectionwastemanagement = db["wastemanagementCollection"]
collectionSolidWaste = db["SolidWaste"]

def loaddata():
  data = pd.read_excel('Data.xlsx'
                      # , sheet_name='2008'
                      , skiprows=1
                      , header=0
                      , skipfooter=1)
  fn = lambda row: str(row.CaseID) + '_' + str(row.City).replace(' ','_') + '_' + str(row.Date) # define a function for the new column


  col = data.apply(fn, axis=1) # get column data with an index
  data = data.assign(custom_cityid=col.values) # assign values to column 'custom_cityid'

  citiesDF = data.filter(['custom_cityid'
  , 'City'
  , 'CityPopulation'
  , 'UrbanPopulation(%of total population)'
  , 'Density(persons/km2)'
  , 'WasteGenerationrate(kg/person/day)'
  , 'Avg GDP(US$/person/year)'
  , 'CO2emission(capita)'
  , 'Ecologicalfootprint(gha/capita)'
  , 'LifeExpectancyboth(years)'
  , 'AdultMortalityrate(probability of dying between the ages of 15 and 60 per 1000 adults)'], axis = 1)

  wastemanagementDF = data.filter(['custom_cityid'
  , 'Extend of plastic waste separation at the municipality level'
  , 'Extend of paper waste separation at the municipality level'
  , 'Extend of metal waste separation at the municipality level'
  , 'Extend of glass waste separation at the municipality level'
  , 'Extend of organic waste separation at the municipality level'
  , 'Extend of battery separation at the municipality level'
  , 'Extend of medical waste separation at the healthcare centers'
  , 'Extend of electric and electronic waste separation at the municipality level'
  , 'Extend of waste dispersed in the city'
  , 'Extend of waste separation at the house level'
  , 'Extend of waste separation at the business level'
  , 'Hazardous waste being treated'
  , 'Frequency of waste collection at commercial sites (times/week)'
  , 'Frequency of waste collection at inner city (times/week)'
  , 'Frequency of waste collection at rural areas (times/week)'], axis = 1)

  solidwasteDF = data.filter(['custom_cityid'
 , 'Total Waste generated(KG)'
 , 'food & organic waste'
 , 'Metal Waste'
 , 'Glass Waste'
 , 'Other Waste'
 , 'Paper Cardboard Waste'
 , 'Plastic Waste'
 , 'Rubber & Leather Waste'
 , 'Wood Waste'
 , 'Yard and Garden Green Waste'], axis = 1)
  
  try:
# To write
    collectionCity.delete_many({})  # Destroy the collection
# To avoid repetitions
    collectionwastemanagement.delete_many({})
    collectionSolidWaste.delete_many({})

    collectionCity.insert_many(citiesDF.to_dict('records'))
    collectionwastemanagement.insert_many(wastemanagementDF.to_dict('records'))
    collectionSolidWaste.insert_many(solidwasteDF.to_dict('records'))

    print("Data was successfully inserted into the respective mongodb collections")
  except Exception as e:
    print(e)

def displaydata():
  
# make a small command i=line interface to accept input as the option and display the output
  print("Please select from the below options(1-7) to get the list of top 3 Cities based on the criteria provided: ")
  print(" 1.Top 3 cities based on the Waste Generation Rate(kg/person/day)")
  print(" 2.Top 3 Cities based on the Avg. GDP in $/person/year")
  print(" 3.Top 3 Cities based on the CO2 Emission/Capita")
  print(" 4.Top 3 Cities based on the Ecological Foot Print/Capita")
  print(" 5.Top 3 Cities based on the Density(persons/km2)")
  print(" 6.Top 3 Cities based on the Life Expectancy rate")
  print(" 7.Top 3 Cities based on the Adult Mortality Rate(probability of dying)")

  input_num = ""

  while input_num != "QUIT":
      input_num = (input("Please enter your choice from 1-7 or enter QUIT to quit the window: "))
      if input_num == "QUIT":
          break

      elif input_num == "1":
          mydoc = collectionCity.find({}, {"_id": 0, "City": 1, "WasteGenerationrate(kg/person/day)": 2}).sort(
          "WasteGenerationrate(kg/person/day)", pymongo.DESCENDING).limit(3)
          for item in mydoc:
              print(item['City'],item['WasteGenerationrate(kg/person/day)'])

      elif input_num == "2":
          mydoc = collectionCity.find({}, {"_id": 0, "City": 1, "Avg GDP(US$/person/year)": 2}).sort(
              "Avg GDP(US$/person/year)", pymongo.DESCENDING).limit(3)
          for item in mydoc:
              print(item['City'],item['Avg GDP(US$/person/year)'])

      elif input_num == "3":
          mydoc = collectionCity.find({}, {"_id": 0, "City": 1, "CO2emission(capita)": 2}).sort(
              "CO2emission(capita)", pymongo.DESCENDING).limit(3)
          for item in mydoc:
              print(item['City'],item['CO2emission(capita)'])

      elif input_num == "4":
          mydoc = collectionCity.find({}, {"_id": 0, "City": 1, "Ecologicalfootprint(gha/capita)": 2}).sort(
              "Ecologicalfootprint(gha/capita)", pymongo.DESCENDING).limit(3)
          for item in mydoc:
              print(item['City'],item['Ecologicalfootprint(gha/capita)'])

      elif input_num == "5":
          mydoc = collectionCity.find({}, {"_id": 0, "City": 1, "Density(persons/km2)": 2}).sort(
              "Density(persons/km2)", pymongo.DESCENDING).limit(3)
          for item in mydoc:
              print(item['City'],item['Density(persons/km2)'])

      elif input_num == "6":
          mydoc = collectionCity.find({}, {"_id": 0, "City": 1, "LifeExpectancyboth(years)": 2}).sort(
              "LifeExpectancyboth(years)", pymongo.DESCENDING).limit(3)
          for item in mydoc:
              print(item['City'],item['LifeExpectancyboth(years)'])

      elif input_num == "7":
          mydoc = collectionCity.find(
              {}, {"_id": 0, "City": 1,
                  "AdultMortalityrate(probability of dying between the ages of 15 and 60 per 1000 adults)": 2}).sort(
                  "AdultMortalityrate(probability of dying between the ages of 15 and 60 per 1000 adults)",
                  pymongo.DESCENDING).limit(3)
          for item in mydoc:

            print(item['City'],item['AdultMortalityrate(probability of dying between the ages of 15 and 60 per 1000 adults)'])

      elif input_num != ["1","2","3","4","5","6","7"]:
          print("Invalid number entered !")

      else:
          break

if __name__ == '__main__':
  loaddata()
  displaydata()




