import json
import os
from datetime import datetime
class TeamBase:
    def __init__(self, db_path='db/teams.json'):
        self.db_path = db_path
        self.teams = self._load_teams()

    def _load_teams(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as file:
                return json.load(file)
        return {}

    def _save_teams(self):
        with open(self.db_path, 'w') as file:
            json.dump(self.teams, file)

    def create_team(self, request: str) -> str:
        team = json.loads(request)
        team_name = team.get("name")

        if len(team_name) > 64:
            raise ValueError("Team name can be max 64 characters.")
        if len(team.get("description", "")) > 128:
            raise ValueError("Description can be max 128 characters.")

        for existing_team in self.teams.values():
            if existing_team["name"] == team_name:
                raise ValueError("Team name must be unique.")

        team_id = str(len(self.teams) + 1)
        team["id"] = team_id
        team["creation_time"] = datetime.now().isoformat()
        self.teams[team_id] = team
        self._save_teams()
        return json.dumps({"id": team_id})

    def list_teams(self) -> str:
        teams_list = [{"name": t["name"], "description": t["description"], "creation_time": t["creation_time"], "admin": t["admin"]} for t in self.teams.values()]
        return json.dumps(teams_list)

    def describe_team(self, request: str) -> str:
        data = json.loads(request)
        team_id = data.get("id")

        if team_id in self.teams:
            team = self.teams[team_id]
            return json.dumps({
                "name": team["name"],
                "description": team["description"],
                "creation_time": team["creation_time"],
                "admin": team["admin"]
            })
        raise ValueError("Team not found.")

    def update_team(self, request: str) -> str:
        data = json.loads(request)
        team_id = data.get("id")
        updated_team = data.get("team")

        if len(updated_team.get("name", "")) > 64:
            raise ValueError("Team name can be max 64 characters.")
        if len(updated_team.get("description", "")) > 128:
            raise ValueError("Description can be max 128 characters.")

        for existing_team in self.teams.values():
            if existing_team["name"] == updated_team["name"] and existing_team["id"] != team_id:
                raise ValueError("Team name must be unique.")

        if team_id in self.teams:
            self.teams[team_id].update(updated_team)
            self._save_teams()
            return json.dumps({"message": "Team updated successfully."})
        raise ValueError("Team not found.")

    def add_users_to_team(self, request: str):
        data = json.loads(request)
        team_id = data.get("id")
        new_users = data.get("users")

        if team_id in self.teams:
            if "users" not in self.teams[team_id]:
                self.teams[team_id]["users"] = []
            if len(self.teams[team_id]["users"]) + len(new_users) > 50:
                raise ValueError("Cannot add more than 50 users to a team.")
            self.teams[team_id]["users"].extend(new_users)
            self._save_teams()
            return json.dumps({"message": "Users added to team successfully."})
        raise ValueError("Team not found.")

    def remove_users_from_team(self, request: str):
        data = json.loads(request)
        team_id = data.get("id")
        remove_users = set(data.get("users"))

        if team_id in self.teams:
            if "users" not in self.teams[team_id]:
                self.teams[team_id]["users"] = []
            self.teams[team_id]["users"] = [u for u in self.teams[team_id]["users"] if u not in remove_users]
            self._save_teams()
            return json.dumps({"message": "Users removed from team successfully."})
        raise ValueError("Team not found.")

    def list_team_users(self, request: str):
        data = json.loads(request)
        team_id = data.get("id")

        if team_id in self.teams:
            users_list = [{"id": u, "name": "user_name", "display_name": "display_name"} for u in self.teams[team_id].get("users", [])]
            return json.dumps(users_list)
        raise ValueError("Team not found.")
