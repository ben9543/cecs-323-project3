from pymongo import MongoClient, database

HOST = "localhost"
PORT = "27017"
DATABASE_URL = f"mongodb://{HOST}:{PORT}"
DATABASE_NAME = "project3"
collections = {
    "adults": "adults",
    "troops": "troops",
    "cookie_types":"cookietypes"
}
def OpenConnection():
    try:
        client = MongoClient(DATABASE_URL)
        return client[DATABASE_NAME]
    except Exception as e:
        print(e)
        return None

def ExecuteAggregation(db, collectionName, pipline):
    try:
        return list(db[collectionName].aggregate(pipline))
    except Exception as e:
        print(e)
        return None

db = OpenConnection()
print(db.list_collection_names())

# collectionName = collections["adults"]
# pipline = [{"$match":{}}]
# test_query = ExecuteAggregation(
#     db=db, 
#     collectionName=collectionName, 
#     pipline=pipline
# )
# print(test_query)