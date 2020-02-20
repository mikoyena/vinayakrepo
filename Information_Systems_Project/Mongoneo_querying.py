# RETRIEVAL PART
from py2neo import Graph, Node, Relationship, cypher
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["WasteManagement"]
collectioncompanies = db["Companies"]

graph = Graph(host='localhost', port=7687, password="davidluiz#32")

# function to get the inputted company details and logic to calculate distances
def get_city_comp_details(cityname):
    citylist=[]
    distlist =[]
    # preprae the query to fetch the list of water processing/water treatment companies located in all the cities
    pipeline=[    
             {"$match":{"Purpose":{"$in":["Water Treatment","Water Processing"]}}},
             {"$project":{"_id":0,"custom_companyid":1,"City":2,"custom_cityid":3,"Company":4,"Purpose":5}}
             ]
    docu = collectioncompanies.aggregate(pipeline)
    for item in docu:
        destcity = item['City']

        #prepare the query to fetch calculate the distance between the source and the destination city
        query ="""Match (a:City),(b:City) where a.name=$cityname and b.name=$destcity
                with point({longitude: a.Longitude, latitude: a.Latitude}) as startpt
                ,point({longitude: b.Longitude, latitude: b.Latitude}) as endpt,a.name as source_cityname,b.name as dest_cityname
                return distance(startpt, endpt)/1000 as traveldistance,source_cityname,dest_cityname
                """
        result=graph.run(query,parameters = {'cityname':cityname,'destcity':destcity}).to_data_frame()
        for row in result.itertuples():
            distlist.append(row.traveldistance)
            citylist.append(row.dest_cityname)
    indx = distlist.index(min(distlist))
    distance = min(distlist)
    nearestcity = citylist[indx]
    print("Nearest city: "+nearestcity+ ", "+"distance: "+str(distance)+" km")

    pipeline=[
             {"$match":{"City":nearestcity}},    
             {"$match":{"Purpose":{"$in":["Water Treatment","Water Processing"]}}},
             {"$project":{"_id":0,"Company":1,"Purpose":2,"Business":3,"Industry":4,"Year founded":5,"employees":6}}
             ]
    docu = collectioncompanies.aggregate(pipeline)
    for item in docu:
        print("Company: "+item['Company'])
        print("Purpose: "+item['Purpose'])
        print("Business: "+item['Business'])
        print("Industry: "+item['Industry'])
        try:
            print("Year founded: "+str(item['Year founded']))
        except Exception as e:
            print("Year founded: not known")
        print("employees: "+str(item['employees'])+"\n")

# end of function here

# function to take inout city from the user
def inpcity():
    flag = ""
    while flag != "quit" :
  
        inpcity = input("Please enter the name of the city to find surrounding water processing companies: ")
        find_query = {"City":inpcity}
        project    = {"_id":0,"custom_companyid":1,"City":2,"custom_cityid":3,"Company":4,"Purpose":5}

        docu = collectioncompanies.find_one(find_query,project)
        if docu == None:
            flag = "goagain"
            print("Invalid city name entered")
        else:
            flag = "quit"
            inpcity = docu['City']


    query ="""
    MATCH (a:City {name:$inpcity})--(b:Company) return b.name as companyname, b.id as companyid
    """

    result = graph.run(query,parameters = {'inpcity':inpcity}).to_data_frame()

    companylist = []
    for row in result.itertuples():
        pipeline=[
        {"$match":{"custom_companyid":row.companyid}},    
        {"$match":{"Purpose":{"$in":["Water Treatment","Water Processing"]}}},
        {"$project":{"_id":0,"Company":1,"Purpose":2,"Business":3,"Industry":4,"Year founded":5,"employees":6}}
        ]
        docu = collectioncompanies.aggregate(pipeline)
        for item in docu:
            print("Company: "+item['Company'])
            print("Purpose: "+item['Purpose'])
            print("Business: "+item['Business'])
            print("Industry: "+item['Industry'])
            try:
                print("Year founded: "+str(item['Year founded']))
            except Exception as e:
                print("Year founded: not known")
            print("employees: "+str(item['employees'])+"\n")
            companylist.append(item)

    numofcomp = (len(companylist))

    if numofcomp == 0:
        print("No Water Processing/water Treatment comapnies found in the city: "+inpcity)
        answer =""
        while answer !="Y" or answer != "N":

            answer = input("Do you want to search for Water Treatment/Water Processing comapnies in the nearby cities?(Type Y for yes and N for No): ")

            if answer != "Y" and answer != "N":
                print("Please enter a valid input (Y or N)")
            if answer == "Y":
                get_city_comp_details(inpcity)
                break        
            if answer == "N":
                break

        
if __name__ == '__main__':
    inpcity()

