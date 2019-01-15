import json

from flask import Flask, request
from flask.json import jsonify

app = Flask(__name__)


class MongoDatabase(object):

    def __init__(self):
        self.users_data = {}
        self.uid = 0

    def add_user(self, user_data):
        self.uid += 1
        self.users_data[self.uid] = user_data

    def get_all_db(self):
        return self.users_data

    def search_user(self, id_data):
        NotImplemented


db = MongoDatabase()


@app.route('/ping', methods=['GET'])
def get_hello():
    test = {}
    test["ping"] = "pong"

    return jsonify(test), 200


@app.route('/users', methods=['POST'])
def add_user():
    user_info = request.get_json()

    db.add_user(user_info)

    response = jsonify(db.get_all_db())

    return response, 200


@app.rout('/users', methods=['GET'])
def get_user():
    user_info = request.get_json()

    try:
        db.search_user(user_info["identifications"])
    except KeyError as e:
        return "Missing identifications", 400


app.run()
