import json
import uuid
from datetime import datetime
from project_board_base import ProjectBoardBase

class ProjectBoardManager(ProjectBoardBase):
    def __init__(self):
        self.board_file = "db/boards.json"
        self.task_file = "db/tasks.json"
        self._load_data()

    def _load_data(self):
        try:
            with open(self.board_file, "r") as f:
                self.boards = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.boards = {}

        try:
            with open(self.task_file, "r") as f:
                self.tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = {}

    def _save_data(self):
        with open(self.board_file, "w") as f:
            json.dump(self.boards, f)
        with open(self.task_file, "w") as f:
            json.dump(self.tasks, f)

    def _is_user_in_team(self, user_id: str, team_id: str) -> bool:
        """Checks if a user belongs to a given team by looking up user_teams.json."""
        try:
            with open("db/user_teams.json", "r") as f:
                user_teams = json.load(f)
                return team_id in user_teams.get(user_id, [])
        except (FileNotFoundError, json.JSONDecodeError):
            return False  # Assume user is not in the team if file is missing or corrupt

    def create_board(self, request: str):
        data = json.loads(request)
        name = data.get("name")
        if not name:
            return json.dumps({"error": "Name is required"})
        description = data.get("description", "")
        team_id = data.get("team_id")
        if not team_id:
            return json.dumps({"error": "Team ID is required"})
        creation_time = data.get("creation_time")
        if not creation_time:
            return json.dumps({"error": "Creation time is required"})

        if len(name) > 64 or len(description) > 128:
            return json.dumps({"error": "Name or description exceeds character limit"})

        # Ensure the team exists
        teams_file = "db/teams.json"
        try:
            with open(teams_file, "r") as f:
                teams = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return json.dumps({"error": "Teams database not found"})

        if team_id not in teams:
            return json.dumps({"error": "Team does not exist"})

        # Ensure board name is unique for the team
        if any(board["name"] == name and board["team_id"] == team_id for board in self.boards.values()):
            return json.dumps({"error": "Board name must be unique for the team"})

        board_id = str(uuid.uuid4())
        self.boards[board_id] = {
            "name": name,
            "description": description,
            "team_id": team_id,
            "creation_time": creation_time,
            "status": "OPEN",
            "tasks": []
        }
        self._save_data()
        return json.dumps({"id": board_id})

    def close_board(self, request: str) -> str:
        data = json.loads(request)
        board_id = data.get("id")
        if not board_id:
            return json.dumps({"error": "Board ID is required"})

        if board_id not in self.boards:
            return json.dumps({"error": "Board not found"})

        board = self.boards[board_id]
        if any(task["status"] != "COMPLETE" for task in self.tasks.values() if task["board_id"] == board_id):
            return json.dumps({"error": "Cannot close board with incomplete tasks"})

        board["status"] = "CLOSED"
        board["end_time"] = datetime.now().isoformat()
        self._save_data()
        return json.dumps({"status": "Board closed successfully"})

    def add_task(self, request: str) -> str:
        data = json.loads(request)
        title = data.get("title")
        if not title:
            return json.dumps({"error": "Title is required"})
        description = data.get("description", "")
        user_id = data.get("user_id")
        if not user_id:
            return json.dumps({"error": "User ID is required"})
        board_id = data.get("board_id")
        if not board_id:
            return json.dumps({"error": "Board ID is required"})

        if len(title) > 64:
            return json.dumps({"error": "Title exceeds character limit of 64"})
            
        if len(description) > 128:
            return json.dumps({"error": "Description exceeds character limit of 64"})

        # Get the team ID for the board
        team_id = self.boards[board_id].get("team_id")
        # Validate if the user is part of the board's team
        if not self._is_user_in_team(user_id, team_id):
            return json.dumps({"error": "User is not a member of the board's team"})

        if board_id not in self.boards or self.boards[board_id]["status"] != "OPEN":
            return json.dumps({"error": "Can only add tasks to an open board"})

        if any(task["title"] == title and task["board_id"] == board_id for task in self.tasks.values()):
            return json.dumps({"error": "Task title must be unique for the board"})

        task_id = str(uuid.uuid4())
        self.tasks[task_id] = {
            "title": title,
            "description": description,
            "user_id": user_id,
            "board_id": board_id,
            "creation_time": datetime.now().isoformat(),
            "status": "OPEN"
        }
        self.boards[board_id]["tasks"].append(task_id)
        self._save_data()
        return json.dumps({"id": task_id})

    def update_task_status(self, request: str):
        data = json.loads(request)
        task_id = data.get("id")
        status = data.get("status")

        if task_id not in self.tasks:
            return json.dumps({"error": "Task not found"})

        if status not in ["OPEN", "IN_PROGRESS", "COMPLETE"]:
            return json.dumps({"error": "Invalid status"})

        self.tasks[task_id]["status"] = status
        self._save_data()
        return json.dumps({"status": "Task status updated successfully"})

    def list_boards(self, request: str) -> str:
        data = json.loads(request)
        team_id = data.get("id")
        if not team_id:
            return json.dumps({"error": "Team ID is required"})

        boards_list = [{"id": board_id, "name": board["name"]}
                       for board_id, board in self.boards.items() if board["team_id"] == team_id and board["status"] == "OPEN"]
        return json.dumps(boards_list)

    def export_board(self, request: str) -> str:
        data = json.loads(request)
        board_id = data.get("id")

        if board_id not in self.boards:
            return json.dumps({"error": "Board not found"})

        board = self.boards[board_id]
        board_info = f"Board Name: {board['name']}\nDescription: {board['description']}\nCreation Time: {board['creation_time']}\nStatus: {board['status']}\n\nTasks:\n"

        for task_id in board["tasks"]:
            task = self.tasks.get(task_id)
            if task:
                board_info += f"- Title: {task['title']}\n  Description: {task['description']}\n  User: {task['user_id']}\n  Status: {task['status']}\n\n"

        out_file = f"out/board_{board_id}.txt"
        with open(out_file, "w") as f:
            f.write(board_info)

        return json.dumps({"out_file": out_file})
