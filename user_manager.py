import os
import json
import uuid

class UserManager:
    def __init__(self, db_file: str = "db/users.json"):
        self.db_file = db_file
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def _save_data(self):
        with open(self.db_file, "w") as f:
            json.dump(self.data, f, indent=2)

    def create_user(self, request: str) -> str:
        request_data = json.loads(request)
        name = request_data.get("name")
        display_name = request_data.get("display_name")
        creation_time = request_data.get("creation_time")

        if not name or len(name) > 64:
            return json.dumps({"error": "User name must be provided and be max 64 characters."})

        if not display_name or len(display_name) > 64:
            return json.dumps({"error": "Display name must be provided and be max 64 characters."})

        if not creation_time:
            return json.dumps({"error": "Creation time must be provided."})

        # Ensure name is unique
        if any(user["name"] == name for user in self.data.values()):
            return json.dumps({"error": "User name must be unique."})

        user_id = str(uuid.uuid4())

        self.data[user_id] = {
            "name": name,
            "display_name": display_name,
            "creation_time": creation_time
        }

        self._save_data()

        return json.dumps({"id": user_id})

    def list_users(self) -> str:
        users_list = [
            {
                "id": user_id,
                "name": user["name"],
                "display_name": user["display_name"],
                "creation_time": user["creation_time"]
            }
            for user_id, user in self.data.items()
        ]
        return json.dumps(users_list, indent=2)

    def describe_user(self, request: str) -> str:
        request_data = json.loads(request)
        user_id = request_data.get("id")
        if not user_id:
            return json.dumps({"error": "User ID must be provided."})

        user = self.data.get(user_id)
        if not user:
            return json.dumps({"error": "User not found."})

        response = {
            "name": user["name"],
            "display_name": user.get("display_name", "Unknown"),
            "creation_time": user["creation_time"]
        }

        return json.dumps(response, indent=2)

    def update_user(self, request: str) -> str:
        request_data = json.loads(request)
        user_id = request_data.get("id")
        if not user_id:
            return json.dumps({"error": "User ID must be provided."})

        updated_user_data = request_data.get("user")
        if not updated_user_data:
            return json.dumps({"error": "User data must be provided."})

        user = self.data.get(user_id)
        if not user:
            return json.dumps({"error": "User not found."})

        if "name" in updated_user_data:
            return json.dumps({"error": "User name cannot be updated."})

        display_name = updated_user_data.get("display_name")
        if display_name and len(display_name) > 64:
            return json.dumps({"error": "Display name must be max 64 characters."})

        self.data[user_id]["display_name"] = display_name
        self._save_data()

        return json.dumps(self.data[user_id])
