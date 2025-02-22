import os
import json
import uuid
from team_base import TeamBase

class TeamManager(TeamBase):
    def __init__(self):
        self.team_file = "db/teams.json"
        self._load_teams()

    def _load_teams(self):
        try:
            with open(self.team_file, "r") as f:
                self.teams = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.teams = {}

    def _save_teams(self):
        with open(self.team_file, "w") as f:
            json.dump(self.teams, f)

    def create_team(self, request: str) -> str:
        data = json.loads(request)
        name = data.get("name")
        if not name:
            return json.dumps({"error": "Team name is required"})
        description = data.get("description", "")
        if not description:
            return json.dumps({"error": "Team description is required"})
        admin = data.get("admin")
        if not admin:
            return json.dumps({"error": "Admin user id is required"})
        creation_time = data.get("creation_time")
        if not creation_time:
            return json.dumps({"error": "Creation time is required"})

        # Load users from users.json
        users_file = "db/users.json"
        if not os.path.exists(users_file):
            return json.dumps({"error": "User database not found"})

        with open(users_file, "r") as f:
            users_data = json.load(f)

        # Check if admin user exists
        if admin not in users_data:
            return json.dumps({"error": "Admin user ID does not exist"})

        if len(name) > 64 or len(description) > 128:
            return json.dumps({"error": "Name or description exceeds character limit"})

        if name in [team["name"] for team in self.teams.values()]:
            return json.dumps({"error": "Team name must be unique"})

        team_id = str(uuid.uuid4())
        self.teams[team_id] = {
            "name": name,
            "description": description,
            "creation_time": creation_time,
            "admin": admin,
            "users": [admin]
        }
        self._save_teams()
        return json.dumps({"id": team_id})

    def list_teams(self) -> str:
        teams_list = [{"name": team["name"], "description": team["description"],
                       "creation_time": team["creation_time"], "admin": team["admin"]}
                      for team in self.teams.values()]
        return json.dumps(teams_list)

    def describe_team(self, request: str) -> str:
        data = json.loads(request)
        team_id = data.get("id")

        if team_id not in self.teams:
            return json.dumps({"error": "Team not found"})

        team = self.teams[team_id]
        response = {
            "name": team["name"],
            "description": team["description"],
            "creation_time": team["creation_time"],
            "admin": team["admin"]
        }

        return json.dumps(response, indent=2)

    def update_team(self, request: str) -> str:
        data = json.loads(request)
        team_id = data.get("id")
        if not team_id:
            return json.dumps({"error": "Team ID is required"})
        updated_team = data.get("team", {})
        if not updated_team:
            return json.dumps({"error": "Team details are required"})

        if team_id not in self.teams:
            return json.dumps({"error": "Team not found"})

        if "name" in updated_team:
            if len(updated_team["name"]) > 64:
                return json.dumps({"error": "Name exceeds character limit"})
            if updated_team["name"] in [team["name"] for team in self.teams.values() if team != self.teams[team_id]]:
                return json.dumps({"error": "Team name must be unique"})
            self.teams[team_id]["name"] = updated_team["name"]

        if "description" in updated_team and len(updated_team["description"]) <= 128:
            self.teams[team_id]["description"] = updated_team["description"]

        if "admin" in updated_team:
            admin_id = updated_team["admin"]
            self.teams[team_id]["admin"] = admin_id

            if admin_id not in self.teams[team_id]["users"]:
                # Add the new admin to the team's users list if they are not already present
                self.teams[team_id]["users"].append(admin_id)

        self._save_teams()
        return json.dumps({"status": "Team updated successfully"})


    def add_users_to_team(self, request: str):
        data = json.loads(request)
        team_id = data.get("id")
        if not team_id:
            return json.dumps({"error": "Team ID is required"})

        users = data.get("users", [])
        if not users:
            return json.dumps({"error": "User IDs are required"})

        if team_id not in self.teams:
            return json.dumps({"error": "Team not found"})

        if len(users) > 50:
            return json.dumps({"error": "Cannot add more than 50 users to a team"})

        current_users = set(self.teams[team_id]["users"])

        # Ensure total users do not exceed 50
        if len(current_users) + len(users) > 50:
            return json.dumps({"error": "Total number of users in a team cannot exceed 50"})

        self.teams[team_id]["users"] = list(current_users.union(users))
        self._save_teams()
        self._generate_user_team_mapping()
        return json.dumps({"status": "Users added successfully"})


    def remove_users_from_team(self, request: str):
        data = json.loads(request)
        team_id = data.get("id")
        if not team_id:
            return json.dumps({"error": "Team ID is required"})
        users = data.get("users", [])
        if not users:
            return json.dumps({"error": "User IDs are required"})

        if team_id not in self.teams:
            return json.dumps({"error": "Team not found"})

        current_users = set(self.teams[team_id]["users"])
        admin_id = self.teams[team_id]["admin"]
        users_to_remove = set(users)

        # We do not want to allow removal of the admin user (assumption)
        # If admin is in the list of users to remove, return an error message.
        if admin_id in users_to_remove:
            return json.dumps({"error": "Admin cannot be removed from the team"})

        self.teams[team_id]["users"] = list(current_users - users_to_remove)

        self._save_teams()
        self._generate_user_team_mapping()
        return json.dumps({"status": "Users removed successfully"})

    def list_team_users(self, request: str):
        data = json.loads(request)
        team_id = data.get("id")

        if team_id not in self.teams:
            return json.dumps({"error": "Team not found"})

        users_file = "db/users.json"
        if not os.path.exists(users_file):
            return json.dumps({"error": "Users database not found"})

        # Load users.json as a dictionary
        with open(users_file, "r") as f:
            users_data = json.load(f)

        # Get the set of user IDs in the team
        team_user_ids = set(self.teams[team_id].get("users", []))
        users_list = [
            {
                "id": user_id,
                "name": users_data[user_id].get("name", "Unknown"),
                "display_name": users_data[user_id].get("display_name", "Unknown")
            }
            for user_id in team_user_ids if user_id in users_data
        ]

        return json.dumps(users_list, indent=2)


    def _generate_user_team_mapping(self, teams_file="db/teams.json", mapping_file="db/user_teams.json"): 
        """
        Generate a mapping of user IDs to team IDs and save it to a file.
        This mapping can be used to quickly find the teams a user belongs to.
        """
        if not os.path.exists(teams_file):
            return

        with open(teams_file, "r") as f:
            teams_data = json.load(f)  

        user_team_map = {}

        # teams_data is a dictionary where keys are team IDs
        for team_id, team in teams_data.items():
            for user_id in team.get("users", []):
                if user_id not in user_team_map:
                    user_team_map[user_id] = []
                user_team_map[user_id].append(team_id)  # Use team_id from key

        with open(mapping_file, "w") as f:
            json.dump(user_team_map, f, indent=2)

