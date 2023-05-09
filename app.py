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
    choice = int(input("Main Menu\n1. Troop Lookup\n2. Scout Lookup\n3. Sales Report\n> "))
    db = OpenConnection()
    if choice == 1:
        troopNum = int(input("Enter Troop Number: "))
        print("----------")
        collectionName = collections["troops"]
        pipline = [{"$match":{"_id": troopNum}}]
        troop = ExecuteAggregation(
            db=db, 
            collectionName=collectionName, 
            pipline=pipline
        )
        print("Troop Number: {}\n- Founding Date: {}\n- Community: {}\n- Number of Scouts: {}\n- Number of Volunteers: {}\nScouts:".format(
            troop[0]["_id"],
            troop[0]["founding_date"],
            troop[0]["community"],
            len(troop[0]["scouts"]),
            len(troop[0]["volunteers"])
        ))
        for scout in troop[0]["scouts"]:
            print("- {}".format(scout["firstname"] + " " + scout["lastname"]))
        print("Volunteers:")
        for volunteer in troop[0]["volunteers"]:
            print("- {} (Position: {})".format(volunteer["firstname"] + " " + volunteer["lastname"], volunteer["position"]))
    elif choice == 2:
        scoutFN = input("Enter Scout First Name: ")
        scoutLN = input("Enter Scout Last Name: ")
        print("----------")
        collectionName = collections["troops"]
        # Since scouts are embedded in troops, you will actually have to select a troop object. But those can be quite large. For full points, you must unwind the scouts array and then match the one unwound document that has the requested name. (You may assume all scout names are unique.)
        pipline = [
            {"$unwind": "$scouts"},
            {"$match": {"scouts.firstname": scoutFN, "scouts.lastname": scoutLN}}
        ]
        scout = ExecuteAggregation(
            db=db,
            collectionName=collectionName,
            pipline=pipline
        )
        scoutFullName = scout[0]["scouts"]["firstname"] + " " + scout[0]["scouts"]["lastname"]
        print("Scout name: {}\n- Birthday: {}\n- Grade Level: {}".format(
            scoutFullName,
            scout[0]["scouts"]["birthday"],
            scout[0]["scouts"]["gradelevel"]
        ))
        print(f"{scoutFullName}'s Adults:")
        for adult in scout[0]["scouts"]["adults"]:
            print("- {}".format(adult["firstname"] + " " + adult["lastname"]))
        print(f"{scoutFullName}'s Allotments:")
        for allotment in scout[0]["scouts"]["allotments"]:
            print("- Delivery Date: {}".format(
                allotment["deliverydate"]
            ))
            for cookie in allotment["cookies"]:
                print("  -{} ({} boxes)".format(
                    cookie["cookietype"],
                    cookie["boxes"]
                ))
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