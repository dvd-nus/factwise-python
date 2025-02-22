import json
from team_manager import TeamManager

def main():
    team_manager = TeamManager()

    while True:
        print("\nOptions:")
        print("1. Create Team")
        print("2. List Teams")
        print("3. Describe Team")
        print("4. Update Team")
        print("5. Add Users to Team")
        print("6. Remove Users from Team")
        print("7. List Team Users")
        print("8. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter team name: ")
            description = input("Enter team description: ")
            admin = input("Enter admin user ID: ")
            creation_time = input("Enter creation time: ")
            request = json.dumps({"name": name, "description": description, "admin": admin, "creation_time": creation_time})
            print(team_manager.create_team(request))

        elif choice == "2":
            print(team_manager.list_teams())

        elif choice == "3":
            team_id = input("Enter team ID: ")
            request = json.dumps({"id": team_id})
            print(team_manager.describe_team(request))

        elif choice == "4":
            team_id = input("Enter team ID: ")
            name = input("Enter new team name (leave blank to keep unchanged): ")
            description = input("Enter new team description (leave blank to keep unchanged): ")
            admin = input("Enter new admin user ID (leave blank to keep unchanged): ")
            update_data = {"id": team_id, "team": {}}
            if name:
                update_data["team"]["name"] = name
            if description:
                update_data["team"]["description"] = description
            if admin:
                update_data["team"]["admin"] = admin
            print(team_manager.update_team(json.dumps(update_data)))

        elif choice == "5":
            team_id = input("Enter team ID: ")
            users = input("Enter user IDs to add (comma-separated): ").split(",")
            request = json.dumps({"id": team_id, "users": users})
            print(team_manager.add_users_to_team(request))

        elif choice == "6":
            team_id = input("Enter team ID: ")
            users = input("Enter user IDs to remove (comma-separated): ").split(",")
            request = json.dumps({"id": team_id, "users": users})
            print(team_manager.remove_users_from_team(request))

        elif choice == "7":
            team_id = input("Enter team ID: ")
            request = json.dumps({"id": team_id})
            print(team_manager.list_team_users(request))

        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
