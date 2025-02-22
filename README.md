# Team Project Planner Tool

## Overview  
This project implements a team project planner tool with APIs for managing users, teams, and project boards. The implementation follows the specifications provided in the base classes (`user_base.py`, `team_base.py`, and `project_board_base.py`). The data is persisted to local file storage to ensure data is available across different sessions.

The APIs support the following features:
- **User Management**: Create, list, describe, and update users.
- **Team Management**: Create, list, describe, update teams, and manage users within a team.
- **Board Management**: Create boards, add tasks, update tasks, and close boards. Boards and tasks adhere to various constraints as defined in the problem statement.

---

## Modules  

The following modules are implemented for handling different aspects of the project:

1. **`user_manager.py`**  
   - Extends the `UserBase` class to implement user management APIs.
   - Manages the creation, listing, description, and updates for users.  
   
2. **`team_manager.py`**  
   - Extends the `TeamBase` class to implement team management APIs.  
   - Provides methods to create teams, manage users in teams, and update team details.

3. **`project_board_manager.py`**  
   - Extends the `ProjectBoardBase` class to implement board and task management APIs.  
   - Manages boards and tasks, ensuring proper validation and constraints are handled.

---

## Data Persistence  
All data is persisted in the `db/` directory as JSON files. Includes
- users.json
- teams.json
- tasks.json
- boards.json
- user_teams.json : a mapping from user id to the team ids that the user is a member of. This is to avoid loading all the teams into memory. This is just for demonstrating one way of optimization as we are assuming the data to be light.

---

## Setup Instructions  
1. Clone the repository or extract the zip file.  
2. Currently, there no extra python libraries are needed to be installed. Skip pip install from requirements.txt
3. To use the APIs, you can use run the scripts starting with the name "run_". <br/>
- User APIs: run_user_manager.py
- Team APIs: run_team_manager.py
- Project Board APIs: run_project_board.py <br/>
Otherwise, import the relevant classes from their respective modules, instantiate them, and call the required methods with the appropriate JSON strings as input.

---

## Assumptions and Design Choices  
- No web framework is being used as it is not explicitly mentioned
- The data being handled is light enough to load the entire json file into memory
- No data storage other than file is to be used. JSON was chosen for simplicity, readability, and ease of serialization. 
- Every API validates input constraints before performing any operation, raising appropriate errors for invalid inputs.  
- Graceful error messages are returned for scenarios like missing IDs, duplicate names, or invalid operations.  
- User should not be allowed to remove the admin of a team
- Changing the team admin to someone who is not present in the team adds them to the team member list. It does not remove the previous admin from the member list
- The APIs will run on a single server instance. File storage access is limited to a single process at a time, ensuring that data is only loaded once when initializing the relevant objects. This simplifies reading data from file storage by avoiding concurrent access issues.
- The board export API always stores the exported data in the file named board_<boardID>.txt. If the board is exported multiple times, it will be overwritten each time.
- The total number of members on a team is restricted to 50

---

## API Details  

### User Management APIs  
1. **`create_user`**: Creates a new user with a unique name.  
2. **`list_users`**: Lists all users.  
3. **`describe_user`**: Provides detailed information about a user.  
4. **`update_user`**: Updates the display name of a user.  
5. **`get_user_teams`**: Lists all teams a user belongs to.

---

### Team Management APIs  
1. **`create_team`**: Creates a new team with a unique name and an admin user.  
2. **`list_teams`**: Lists all teams.  
3. **`describe_team`**: Provides detailed information about a team.  
4. **`update_team`**: Updates team details.  
5. **`add_users_to_team`**: Adds users to a team (capped at 50 users).  
6. **`remove_users_from_team`**: Removes users from a team.  
7. **`list_team_users`**: Lists all users in a team.

---

### Board Management APIs  
1. **`create_board`**: Creates a new board for a team with a unique name.  
2. **`close_board`**: Closes a board if all tasks are complete.  
3. **`add_task`**: Adds a task to an open board.  
4. **`update_task_status`**: Updates the status of a task.  
5. **`list_boards`**: Lists all open boards for a team.  
6. **`export_board`**: Exports a board and its tasks to a text file. 

---