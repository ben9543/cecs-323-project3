from pymongo import MongoClient

DATABASE_URL = "mongodb+srv://cecs327assignment:cecs327assignment@cluster0.bsjkxmo.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "project3"


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
    choice = -1
    db = OpenConnection()
    while choice != 0:
        choice = int(
            input(
                "Main Menu\n0. Exit\n1. Troop Lookup\n2. Scout Lookup\n3. Sales Report\n> "
            )
        )
        if choice == 1:
            troopNum = int(input("Enter Troop Number: "))
            print("----------")
            pipline = [{"$match": {"_id": troopNum}}]
            troop = ExecuteAggregation(db=db, collectionName="troops", pipline=pipline)
            print(
                "Troop Number: {}\n- Founding Date: {}\n- Community: {}\n- Number of Scouts: {}\n- Number of Volunteers: {}\nScouts:".format(
                    troop[0]["_id"],
                    troop[0]["founding_date"],
                    troop[0]["community"],
                    len(troop[0]["scouts"]),
                    len(troop[0]["volunteers"]),
                )
            )
            for scout in troop[0]["scouts"]:
                print("- {}".format(scout["firstname"] + " " + scout["lastname"]))
            print("Volunteers:")
            for volunteer in troop[0]["volunteers"]:
                print(
                    "- {} (Position: {})".format(
                        volunteer["firstname"] + " " + volunteer["lastname"],
                        volunteer["position"],
                    )
                )
            print("----------")
        elif choice == 2:
            scoutFN = input("Enter Scout First Name: ")
            scoutLN = input("Enter Scout Last Name: ")
            print("----------")
            pipline = [
                {"$unwind": "$scouts"},
                {
                    "$match": {
                        "scouts.firstname": scoutFN,
                        "scouts.lastname": scoutLN,
                    },
                },
            ]
            scout = ExecuteAggregation(db=db, collectionName="troops", pipline=pipline)
            scoutFullName = (
                scout[0]["scouts"]["firstname"] + " " + scout[0]["scouts"]["lastname"]
            )
            print(
                "Scout name: {}\n- Birthday: {}\n- Grade Level: {}".format(
                    scoutFullName,
                    scout[0]["scouts"]["birthday"],
                    scout[0]["scouts"]["gradelevel"],
                )
            )
            print(f"{scoutFullName}'s Adults:")
            for adult in scout[0]["scouts"]["adults"]:
                print("- {}".format(adult["firstname"] + " " + adult["lastname"]))
            print(f"{scoutFullName}'s Allotments:")
            for allotment in scout[0]["scouts"]["allotments"]:
                print("- Delivery Date: {}".format(allotment["deliverydate"]))
                for cookie in allotment["cookies"]:
                    print(
                        "  -{} ({} boxes)".format(cookie["cookietype"], cookie["boxes"])
                    )
            print("----------")
        elif choice == 3:
            troopNum = int(input("Enter Troop Number: "))
            print("----------")
            pipline = [
                {"$match": {"_id": troopNum}},
                {"$unwind": "$scouts"},
                {"$unwind": "$scouts.allotments"},
                {"$unwind": "$scouts.allotments.cookies"},
                {
                    "$lookup": {
                        "from": "cookietypes",
                        "localField": "scouts.allotments.cookies.cookietype",
                        "foreignField": "name",
                        "as": "cookie",
                    },
                },
                {"$unwind": "$cookie"},
                {
                    "$project": {
                        "firstname": "$scouts.firstname",
                        "lastname": "$scouts.lastname",
                        "totalvalue": {
                            "$multiply": [
                                "$scouts.allotments.cookies.boxes",
                                "$cookie.price",
                            ],
                        },
                    },
                },
                {
                    "$group": {
                        "_id": {
                            "firstname": "$firstname",
                            "lastname": "$lastname",
                        },
                        "totalvalue": {"$sum": "$totalvalue"},
                    },
                },
            ]
            salesReport = ExecuteAggregation(
                db=db, collectionName="troops", pipline=pipline
            )
            print("Sales Report for Troop {}".format(troopNum))
            for scout in salesReport:
                print(
                    "- {}: ${}".format(
                        scout["_id"]["firstname"] + " " + scout["_id"]["lastname"],
                        scout["totalvalue"],
                    )
                )
            print("----------")
        else:
            if choice != 0:
                print("Invalid Choice, try again")
                while choice != 1 and choice != 2 and choice != 3:
                    choice = int(
                        input(
                            "Main Menu\n1. Troop Lookup\n2. Scout Lookup\n3. Sales Report\n>"
                        )
                    )
            else:
                print("----------\nGoodbye! :)")


if __name__ == "__main__":
    main()
