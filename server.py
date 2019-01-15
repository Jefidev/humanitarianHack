from database import MongoDatabase
from flask import Flask, request
from flask.json import jsonify

app = Flask(__name__)

db = MongoDatabase()


@app.route('/ping', methods=['GET'])
def get_hello():
    test = {}
    test["ping"] = "pong"

    return jsonify(test), 200


@app.route('/users', methods=['POST'])
def add_user():
    user_info = request.get_json()

    # Did the user have at least one authentication methods
    if "identifications" not in user_info:
        return jsonify({"error": "The new user should have at least one identification method"}), 400

    if len(user_info["identifications"]) == 0:
        return jsonify({"error": "The new user should have at least one identification method"}), 400

    db.add_user(user_info)
    return "success", 200


@app.route('/users/search', methods=['POST'])
def get_user():
    user_info = request.get_json()

    try:
        res = db.search_user(user_info["identifications"])

        print(res)

        if len(res) == 0:
            return jsonify({"error": "No user found"}), 400

        res.sort(key=lambda x: x["percentage"])
        found = res[0]
        print(found)
        return jsonify(found), 200

    except KeyError as e:
        return jsonify({"error": "Missing identifications"}), 400


app.run()
