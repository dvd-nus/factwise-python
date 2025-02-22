import json
import os
from user_manager import UserManager  # Assuming UserManager is in user_manager.py

def main():
    user_manager = UserManager()
    
    while True:
        print("\nOptions:")
        print("1. Create User")
        print("2. List Users")
        print("3. Describe User")
        print("4. Update User")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter name: ")
            display_name = input("Enter display name: ")
            creation_time = input("Enter creation time: ")
            request = json.dumps({"name": name, "display_name": display_name, "creation_time": creation_time})
            print("Response:", user_manager.create_user(request))
        
        elif choice == "2":
            print("Users:", user_manager.list_users())
        
        elif choice == "3":
            user_id = input("Enter User ID: ")
            request = json.dumps({"id": user_id})
            print("Response:", user_manager.describe_user(request))
        
        elif choice == "4":
            user_id = input("Enter User ID: ")
            display_name = input("Enter new display name: ")
            request = json.dumps({"id": user_id, "user": {"display_name": display_name}})
            print("Response:", user_manager.update_user(request))
        
        elif choice == "5":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
