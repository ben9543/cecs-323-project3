from pymongo import MongoClient, database

# HOST = "localhost"
# PORT = "27017"
# DATABASE_URL = f"mongodb://{HOST}:{PORT}"
DATABASE_URL = "mongodb+srv://cecs327assignment:cecs327assignment@cluster0.bsjkxmo.mongodb.net/?retryWrites=true&w=majority"
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

def main():
    choice = int(input("Main Menu\n1. Troop Lookup\n2. Scout Lookup\n3. Sales Report\n>"))
    if choice == 1:
        troopNum = int(input("Enter Troop Number: "))
        db = OpenConnection()
        collectionName = collections["troops"]
        pipline = [{"$match":{"_id": troopNum}}]
        troop = ExecuteAggregation(
            db=db, 
            collectionName=collectionName, 
            pipline=pipline
        )
        print("\nTroop Number: {}\n- Founding Date: {}\n- Community: {}\n- Number of Scouts: {}\n- Number of Volunteers: {}\nScouts:".format(
            troop[0]["_id"],
            troop[0]["founding_date"],
            troop[0]["community"],
            len(troop[0]["scouts"]),
            len(troop[0]["volunteers"])
        ))
        for scout in troop[0]["scouts"]:
            print("- Name: {}".format(scout["firstname"] + " " + scout["lastname"]))
        print("Volunteers:")
        for volunteer in troop[0]["volunteers"]:
            print("- Name: {} (Position: {})".format(volunteer["firstname"] + " " + volunteer["lastname"], volunteer["position"]))
    elif choice == 2:
        pass
    elif choice == 3:
        pass
    else:
        print("Invalid Choice, try again")
        while choice != 1 and choice != 2 and choice != 3:
            choice = int(input("Main Menu\n1. Troop Lookup\n2. Scout Lookup\n3. Sales Report\n>"))

if __name__ == "__main__":
    main()

# db = OpenConnection()
# print(db.list_collection_names())

# collectionName = collections["adults"]
# pipline = [{"$match":{}}]
# test_query = ExecuteAggregation(
#     db=db, 
#     collectionName=collectionName, 
#     pipline=pipline
# )
# print(test_query)