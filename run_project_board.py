import json
from project_board_manager import ProjectBoardManager

def main():
    manager = ProjectBoardManager()
    
    while True:
        print("\nAvailable operations:")
        print("1. Create Board")
        print("2. Close Board")
        print("3. Add Task")
        print("4. Update Task Status")
        print("5. List Boards")
        print("6. Export Board")
        print("7. Exit")
        
        choice = input("Enter choice (1-7): ")
        
        if choice == "1":
            name = input("Enter board name: ")
            description = input("Enter board description: ")
            team_id = input("Enter team ID: ")
            creation_time = input("Enter creation time (ISO format): ")
            request = json.dumps({"name": name, "description": description, "team_id": team_id, "creation_time": creation_time})
            print(manager.create_board(request))
        
        elif choice == "2":
            board_id = input("Enter board ID to close: ")
            request = json.dumps({"id": board_id})
            print(manager.close_board(request))
        
        elif choice == "3":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            user_id = input("Enter user ID: ")
            board_id = input("Enter board ID: ")
            request = json.dumps({"title": title, "description": description, "user_id": user_id, "board_id": board_id})
            print(manager.add_task(request))
        
        elif choice == "4":
            task_id = input("Enter task ID: ")
            status = input("Enter new status (OPEN, IN_PROGRESS, COMPLETE): ")
            request = json.dumps({"id": task_id, "status": status})
            print(manager.update_task_status(request))
        
        elif choice == "5":
            team_id = input("Enter team ID to list boards: ")
            request = json.dumps({"id": team_id})
            print(manager.list_boards(request))
        
        elif choice == "6":
            board_id = input("Enter board ID to export: ")
            request = json.dumps({"id": board_id})
            print(manager.export_board(request))
        
        elif choice == "7":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
