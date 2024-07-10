import json
import os
from datetime import datetime

class ProjectBoardBase:
    def __init__(self, db_path='db/boards.json'):
        self.db_path = db_path
        self.boards = self._load_boards()

    def _load_boards(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as file:
                return json.load(file)
        return {}

    def _save_boards(self):
        with open(self.db_path, 'w') as file:
            json.dump(self.boards, file)

    def create_board(self, request: str):
        board = json.loads(request)
        team_id = board.get("team_id")
        board_name = board.get("name")

        if len(board_name) > 64:
            return json.dumps({"error": "Board name can be max 64 characters."})
        if len(board.get("description", "")) > 128:
            return json.dumps({"error": "Description can be max 128 characters."})

        if team_id not in self.boards:
            self.boards[team_id] = []

        for b in self.boards[team_id]:
            if b["name"] == board_name:
                return json.dumps({"error": "Board name must be unique for a team."})

        board_id = str(len(self.boards[team_id]) + 1)
        board["id"] = board_id
        board["status"] = "OPEN"
        self.boards[team_id].append(board)
        self._save_boards()
        return json.dumps({"id": board_id})

    def close_board(self, request: str) -> str:
        data = json.loads(request)
        board_id = data.get("id")
        
        for team_boards in self.boards.values():
            for board in team_boards:
                if board["id"] == board_id:
                    if all(task["status"] == "COMPLETE" for task in board.get("tasks", [])):
                        board["status"] = "CLOSED"
                        board["end_time"] = datetime.now().isoformat()
                        self._save_boards()
                        return json.dumps({"message": "Board closed successfully."})
                    else:
                        return json.dumps({"error": "All tasks must be marked as COMPLETE to close the board."})
        return json.dumps({"error": "Board not found."})

    def add_task(self, request: str) -> str:
        task = json.loads(request)
        board_id = task.get("board_id")
        task_title = task.get("title")

        if len(task_title) > 64:
            return json.dumps({"error": "Task title can be max 64 characters."})
        if len(task.get("description", "")) > 128:
            return json.dumps({"error": "Description can be max 128 characters."})

        for team_boards in self.boards.values():
            for board in team_boards:
                if board["id"] == board_id:
                    if board["status"] != "OPEN":
                        return json.dumps({"error": "Can only add task to an OPEN board."})
                    if "tasks" not in board:
                        board["tasks"] = []
                    if any(t["title"] == task_title for t in board["tasks"]):
                        return json.dumps({"error": "Task title must be unique for a board."})
                    
                    task_id = str(len(board["tasks"]) + 1)
                    task["id"] = task_id
                    task["status"] = "OPEN"
                    board["tasks"].append(task)
                    self._save_boards()
                    return json.dumps({"id": task_id})

        return json.dumps({"error": "Board not found."})

    def update_task_status(self, request: str):
        data = json.loads(request)
        task_id = data.get("id")
        new_status = data.get("status")

        for team_boards in self.boards.values():
            for board in team_boards:
                for task in board.get("tasks", []):
                    if task["id"] == task_id:
                        task["status"] = new_status
                        self._save_boards()
                        return json.dumps({"message": "Task status updated successfully."})
        return json.dumps({"error": "Task not found."})

    def list_boards(self, request: str) -> str:
        data = json.loads(request)
        team_id = data.get("id")
        if team_id not in self.boards:
            return json.dumps([])
        open_boards = [{"id": b["id"], "name": b["name"]} for b in self.boards[team_id] if b["status"] == "OPEN"]
        return json.dumps(open_boards)

    def export_board(self, request: str) -> str:
        data = json.loads(request)
        board_id = data.get("id")

        for team_boards in self.boards.values():
            for board in team_boards:
                if board["id"] == board_id:
                    file_name = f"out/board_{board_id}.txt"
                    with open(file_name, 'w') as file:
                        file.write(f"Board Name: {board['name']}\n")
                        file.write(f"Description: {board['description']}\n")
                        file.write(f"Team ID: {board['team_id']}\n")
                        file.write(f"Creation Time: {board['creation_time']}\n")
                        file.write(f"Status: {board['status']}\n")
                        if "end_time" in board:
                            file.write(f"End Time: {board['end_time']}\n")
                        file.write("\nTasks:\n")
                        for task in board.get("tasks", []):
                            file.write(f"  Task ID: {task['id']}\n")
                            file.write(f"  Title: {task['title']}\n")
                            file.write(f"  Description: {task['description']}\n")
                            file.write(f"  User ID: {task['user_id']}\n")
                            file.write(f"  Creation Time: {task['creation_time']}\n")
                            file.write(f"  Status: {task['status']}\n")
                            file.write("\n")
                    return json.dumps({"out_file": file_name})

        return json.dumps({"error": "Board not found."})
