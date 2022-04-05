
from flask import Flask, Response, request
app = Flask(__name__)
import pymongo
from bson.objectid import ObjectId
import json


###########################################################################


try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.company
    mongo.server_info() # trigger exception if cannot connect to database
except:
    print("ERROR - Cannot connect to db")


###########################################################################


@app.route("/users", methods=["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(response=json.dumps(data),
        status=200,
        mimetype="application/json")

    except Exception as ex:
        print(ex)
        Response(response=json.dumps({"message": "cannot read users"}),status=500,mimetype="application/json")


###########################################################################


@app.route("/users", methods=["POST"])
def create_user():
    try:
        user = {
            "name": request.form["name"],
            "lastName": request.form["lastName"]
        }
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
        #for attr in dir(dbResponse):
            # print(attr)
        return Response(
            response=json.dumps(
                {"message": "user created", 
                "id":f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )

    except Exception as ex:
        print(ex)


###########################################################################
if __name__ == "__main__":
    app.run(port=80, debug=True)

