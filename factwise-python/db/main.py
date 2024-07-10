# main.py
from team_impl import TeamBase
from user_impl import UserBase

def main():

    user_handler = UserBase()

    
    user_request = '{"name": "user1", "display_name": "User One"}'
    created_user = user_handler.create_user(user_request)
    print("Created User:", created_user)

    
    users_list = user_handler.list_users()
    print("List of Users:", users_list)

if __name__ == "__main__":
    main()