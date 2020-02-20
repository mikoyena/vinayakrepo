import pandas as pd
from pprint import pprint
from py2neo import Graph, Node, Relationship, cypher

def loadneonodes():
    graph = Graph(host='localhost', port=7687, password="davidluiz#32")

    #delete all the existing nodes
    graph.delete_all()

    #Read the csv file to load the CIty nodes
    query = """
    LOAD CSV WITH HEADERS FROM 'file:///C:/Users/Vinayak/neo4j-community-3.5.12/import/City_load_data.CSV' AS row
    CREATE (c:City {name:row.City,id:row.custom_cityid , Latitude:toFloat(row.Latitude), Longitude:toFloat(row.Longitude)})
    """

    graph.run(query)

    # Read the csv fle to load company nodes
    query = """
    LOAD CSV WITH HEADERS FROM 'file:///C:/Users/Vinayak/neo4j-community-3.5.12/import/Company_load_data.csv' AS row
    CREATE (cp:Company {name:row.Company,id:row.custom_companyid,custom_cityid:row.custom_cityid })
    """

    graph.run(query)

    # Read the csv file to load the relationship between company and cities
    query="""
    LOAD CSV WITH HEADERS FROM 'file:///C:/Users/Vinayak/neo4j-community-3.5.12/import/Relation_bw_comp_City.csv' AS row
    MATCH (cp:Company { id: row.custom_companyid}),(c:City { id: row.custom_cityid})
    CREATE (cp)-[:BELONGS { role: row.Belongs_to }]->(c)
    """

    graph.run(query)

def loaddata():
    
    # read the data of the companies to fetch the key from the mongodb.
    data = pd.read_csv('Trade_data_csv1.csv')

    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017/")
    db = client["WasteManagement"]
    collectionCity = db["Cities"]
    collectionCompany = db["Companies"]

    for row in data.itertuples():
        find_query = {"City": row.City}
        project = {"_id":0, "custom_cityid":1}
        docu = list(collectionCity.find(find_query,project))
        for item in docu:
            data.loc[row.Index, "custom_cityid"] = item['custom_cityid']

    fn1= lambda row: str(row.Company).replace(' ','_') + '_' + str(row.ID) + '_' + str(row.City).replace(' ','_')
    col1 = data.apply(fn1,axis=1)
    data = data.assign(custom_companyid=col1.values)

    # create the dataframe to load the company data and write in into a csv file
    companiescsvDF = data.filter(['custom_companyid','Company','custom_cityid'])

    companiescsvDF.to_csv(r'C:\Users\Vinayak\neo4j-community-3.5.12\import\Company_load_data.CSV',
                header =True ,
                index=None,
                encoding='utf-8-sig')

    print("""the Company data CSV file was successfully created and was placed in the folder:"C:/Users/Vinayak/neo4j-community-3.5.12/import" """)

    reltnDF = data.filter(['custom_companyid','custom_cityid'])
    reltnDF['Belongs to']='this city'

    reltnDF.to_csv(r'C:\Users\Vinayak\neo4j-community-3.5.12\import\Relation_bw_comp_City.CSV',
                header =True,
                index =None,
                encoding ='utf-8-sig')

    print("""the Relationship data CSV file was successfully created and was placed in the folder:"C:/Users/Vinayak/neo4j-community-3.5.12/import" """)

    # create the dataframe to load the relationship data between companies and cities and write in into a csv file
    companies_df = data.filter(['custom_companyid','custom_cityid','Company','Business','Industry','Purpose','City',
                'Market focus','Year founded','employees'],axis=1)


    db = client["WasteManagement"]

    collectioncompanies = db["Companies"]

    collectioncompanies.delete_many({})

    collectioncompanies.insert_many(companies_df.to_dict('records'))

    print("The records were successfully inserted into MongoDB database into collection: Companies")

    # read the data of the cities to fetch the latitude and longitude information and write it into a csv file.
    data = pd.read_excel('Data.xlsx',
        skiprows=1,skipfooter=1)

    fn = lambda row: str(row.CaseID) + '_' + str(row.City).replace(' ','_') + '_' + str(row.Date) # define a function for the new column
    col = data.apply(fn, axis=1) # get column data with an index
    data = data.assign(custom_cityid=col.values) # assign values to column 'custom_cityid'

    citycsvDF = data.filter(['custom_cityid','City','Latitude','Longitude'],axis=1)

    citycsvDF.to_csv(r'C:\Users\Vinayak\neo4j-community-3.5.12\import\City_load_data.CSV',
    header=True,
    index=None,
    encoding='utf-8-sig')

    print("""the City data CSV file was successfully created and was placed in the folder:"C:/Users/Vinayak/neo4j-community-3.5.12/import" """)

# start 
if __name__ == '__main__':
    loaddata()
    loadneonodes()




        