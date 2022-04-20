
import json
from bson.objectid import ObjectId
import pymongo
from flask import Flask, Response, request
app = Flask(__name__)


###########################################################################


try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS=1000
    )
    db = mongo.company
    mongo.server_info()  # trigger exception if cannot connect to database
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
        Response(response=json.dumps(
            {"message": "cannot read users"}), status=500, mimetype="application/json")


###########################################################################


@app.route("/users/<id>", methods=["PATCH"])
def update_users(id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "name": request.form["name"],
                "lastName": request.form["lastName"]
            }}
        )

        if dbResponse.modified_count == 1:
            return Response(
                response=json.dumps(
                    {"message": "User updated"}
                ), status=200,
                mimetype="application/json"
            )

        else:
            return Response(
                response=json.dumps(
                    {"message": "Nothing to update"}
                ), status=200,
                mimetype="application/json"
            )

    except Exception as ex:
        print("********************")
        print(ex)
        print("********************")
        return Response(
            response=json.dumps(
                {"message": "sorry cannot update!!"}
            ), status=500,
            mimetype="application/json"
        )


###########################################################################


@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):

    try:

        dbResponse = db.users.delete_one(
            {"_id": ObjectId(id)}
        )

        for attr in dir(dbResponse):
            print("******{attr}*******")
        return Response(
            response=json.dumps(
                {"message": "User Deleted", "id": f"{id}"}
            ), status=200,
            mimetype="application/json"
        )

    except Exception as ex:

        print("********************")
        print(ex)
        print("********************")
        return Response(
            response=json.dumps(
                {"message": "sorry cannot delete!!"}
            ), status=500,
            mimetype="application/json"
        )


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
        # for attr in dir(dbResponse):
        # print(attr)
        return Response(
            response=json.dumps(
                {"message": "user created",
                 "id": f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )

    except Exception as ex:
        print(ex)


###########################################################################
if __name__ == "__main__":
    app.run(port=80, debug=True)
