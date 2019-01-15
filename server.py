import datetime
import os

import jwt
from database import MongoDatabase
from flask import Flask, request
from flask.json import jsonify
from flask_cors import CORS, cross_origin

idam = os.environ.get('ID_AMAZON', None)
keyam = os.environ.get('KEY_AMAZON', None)


application = Flask(__name__)
CORS(application, support_credentials=True)

db = MongoDatabase(idam, keyam)
SECRET = "chjxwk<lmksfhjsckdlxsckdlhjkscdlcjvvblcdsfjbgkd,slq"


@application.route('/ping', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_hello():
    test = {}
    test["ping"] = "pong"

    return jsonify(test), 200


'''
Add a user to the database with, at least, 1 identification methods
'''


@application.route('/users', methods=['POST'])
@cross_origin(supports_credentials=True)
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


@application.route('/users/search', methods=['POST'])
@cross_origin(supports_credentials=True)
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


@application.route('/users/authenticate', methods=["POST"])
@cross_origin(supports_credentials=True)
def authenticate_user():
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


@application.route('/users', methods=["DELETE"])
@cross_origin(supports_credentials=True)
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


@application.route('/users', methods=["PUT"])
@cross_origin(supports_credentials=True)
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


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80, debug=True)
