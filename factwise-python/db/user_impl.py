import json
import os
from datetime import datetime

class UserBase:
    def __init__(self, db_path='db/users.json'):
        self.db_path = db_path
        self.users = self._load_users()

    def _load_users(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as file:
                return json.load(file)
        return {}

    def _save_users(self):
        with open(self.db_path, 'w') as file:
            json.dump(self.users, file)

    def create_user(self, request: str) -> str:
        user = json.loads(request)
        user_name = user.get("name")

        if len(user_name) > 64:
            raise ValueError("User name can be max 64 characters.")
        if len(user.get("display_name", "")) > 64:
            raise ValueError("Display name can be max 64 characters.")

        for existing_user in self.users.values():
            if existing_user["name"] == user_name:
                raise ValueError("User name must be unique.")

        user_id = str(len(self.users) + 1)
        user["id"] = user_id
        user["creation_time"] = datetime.now().isoformat()
        self.users[user_id] = user
        self._save_users()
        return json.dumps({"id": user_id})

    def list_users(self) -> str:
        users_list = [{"name": u["name"], "display_name": u["display_name"], "creation_time": u["creation_time"]} for u in self.users.values()]
        return json.dumps(users_list)

    def describe_user(self, request: str) -> str:
        data = json.loads(request)
        user_id = data.get("id")

        if user_id in self.users:
            user = self.users[user_id]
            return json.dumps({
                "name": user["name"],
                "display_name": user["display_name"],
                "creation_time": user["creation_time"]
            })
        raise ValueError("User not found.")

    def update_user(self, request: str) -> str:
        data = json.loads(request)
        user_id = data.get("id")
        updated_user = data.get("user")

        if len(updated_user.get("display_name", "")) > 64:
            raise ValueError("Display name can be max 64 characters.")

        if user_id in self.users:
            self.users[user_id]["display_name"] = updated_user.get("display_name", self.users[user_id]["display_name"])
            self._save_users()
            return json.dumps({"message": "User updated successfully."})
        raise ValueError("User not found.")

    def get_user_teams(self, request: str) -> str:
        data = json.loads(request)
        user_id = data.get("id")

        teams = []
        if os.path.exists('db/teams.json'):
            with open('db/teams.json', 'r') as file:
                all_teams = json.load(file)
                for team in all_teams.values():
                    if "users" in team and user_id in team["users"]:
                        teams.append({
                            "name": team["name"],
                            "description": team["description"],
                            "creation_time": team["creation_time"]
                        })
        return json.dumps(teams)
