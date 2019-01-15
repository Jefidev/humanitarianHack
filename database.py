import json
from pathlib import Path


class MongoDatabase(object):

    def __init__(self):
        self.users_data = {}
        self.uid = 0

        # load data
        my_file = Path("data.json")
        if my_file.is_file():
            with open('data.json', 'r') as f:
                self.users_data = json.loads(f.read())

            self.uid = max(self.users_data.keys())

    def add_user(self, user_data):
        self.uid += 1
        self.users_data[self.uid] = user_data

        with open('data.json', 'w') as outfile:
            json.dump(self.users_data, outfile)

    def get_all_db(self):
        return self.users_data

    def search_user(self, id_data):
        found = []
        ids = []

        for uid in self.users_data:
            user = self.users_data[uid]

            score = self._id_match(user, id_data)
            percentage = score / len(id_data)

            if percentage > 0:
                found.append({
                    'user': user,
                    'percentage': percentage
                })

                ids.append(uid)

        return found, ids

    def _id_match(self, user, id_data):

        match = 0
        user_available_id = user["identifications"]

        for key in user_available_id:
            if key in id_data:

                if user_available_id[key] == id_data[key]:
                    match += 1

        return match

    def get_unique_users(self, id_data):
        found, ids = self.search_user(id_data)

        if len(found) == 1:
            return found[0], ids[0]

        raise ModuleNotFoundError
