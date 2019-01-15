import datetime

import jwt
from database import MongoDatabase
from flask import Flask, request
from flask.json import jsonify

app = Flask(__name__)

db = MongoDatabase()
SECRET = "chjxwk<lmksfhjsckdlxsckdlhjkscdlcjvvblcdsfjbgkd,slq"


@app.route('/ping', methods=['GET'])
def get_hello():
    test = {}
    test["ping"] = "pong"

    return jsonify(test), 200


'''
Add a user to the database with, at least, 1 identification methods
'''


@app.route('/users', methods=['POST'])
def add_user():
    user_info = request.get_json()

    # Did the user have at least one authentication methods
    if "identifications" not in user_info:
        return jsonify({"error": "The new user should have at least one identification method"}), 400

    if len(user_info["identifications"]) < 3:
        return jsonify({"error": "The new user should have at least one identification method"}), 400

    user_info["parameters"] = {}
    db.add_user(user_info)
    return "success", 200


'''
Search the most probable user based on the identification methodes provided.
'''


@app.route('/users/search', methods=['POST'])
def get_user():
    user_info = request.get_json()

    try:
        res, _ = db.search_user(user_info["identifications"])

        if len(res) == 0:
            return jsonify({"error": "No user found"}), 400

        res.sort(key=lambda x: x["percentage"])
        found = res[0]
        return jsonify(found), 200

    except KeyError as e:
        return jsonify({"error": "Missing identifications"}), 400


@app.route('/users/authenticate', methods=["POST"])
def authenticate_user(self):
    user_id = request.get_json()

    try:
        u, uid = db.get_unique_users(user_id)

        encoded_jwt = jwt.encode(
            {'UID': uid, 'exp': datetime.datetime.utcnow() +
             datetime.timedelta(minute=10)},
            SECRET, algorithm='HS256')

        return jsonify({"jwt": encoded_jwt, "user": u}), 200

    except ModuleNotFoundError:
        return jsonify({"error": "No matching in DB"}), 400


@app.route('/users', methods=["DELETE"])
def delete_data():
    delete_info = request.get_json()

    try:
        data = jwt.decode(delete_info["jwt"], SECRET, algorithms=['HS256'])
        db.delete_user_data(data["UID"], delete_info["delete_cat"])

        return "success", 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 400
    except KeyError as e:
        return jsonify({"error": "Missing key (expect jwt, category to delete"}), 400


@app.route('/users', methods=["PUT"])
def update_data():
    update_info = request.get_json()

    try:
        data = jwt.decode(update_info["jwt"], SECRET, algorithms=['HS256'])
        db.update_user_data(data["UID"], update_info["payload"])

        return "success", 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 400
    except KeyError as e:
        return jsonify({"error": "Missing key (expect jwt, payload"}), 400


app.run()
