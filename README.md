Project Management Tool
This project is a simple project management tool implemented in Python, providing APIs to manage users, teams, and project boards. It uses local file storage to persist data.

Features
User Management:

Create, list, describe, and update users.
Retrieve teams associated with a user.
Team Management:

Create, list, describe, update teams.
Add or remove users from teams.
List users belonging to a team.
Project Board Management:

Create, list, and close project boards.
Add tasks to boards and update task statuses.
Export boards to a text file.
Requirements
Python 3.x
JSON
Basic file handling knowledge
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/project-management-tool.git
cd project-management-tool
Install dependencies (not required for this project).

Run the project:

bash
Copy code
python main.py
Usage
User Management:

Use APIs in user_impl.py to manage users.
Team Management:

Use APIs in team_impl.py to manage teams.
Project Board Management:

Use APIs in project_board_impl.py to manage project boards and tasks.
File Structure
main.py: Entry point of the application.
user_impl.py: Implements user management APIs.
team_impl.py: Implements team management APIs.
project_board_impl.py: Implements project board management APIs.
db/: Directory containing JSON files for data storage (users.json, teams.json, etc.).
Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
This project was inspired by the need for a simple project management tool.
Thanks to OpenAI for providing ChatGPT, which assisted in developing this README.
