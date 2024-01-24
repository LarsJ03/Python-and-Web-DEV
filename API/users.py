# user.py
import json
import os


class Users:
    CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    USERS_FILE = os.path.join(CURRENT_DIRECTORY, 'users.json')

    @staticmethod
    def load_users():
        if not os.path.exists(Users.USERS_FILE):
            return []
        with open(Users.USERS_FILE, 'r') as file:
            return json.load(file)

    @staticmethod
    def save_users(users):
        with open(Users.USERS_FILE, 'w') as file:
            json.dump(users, file, indent=4)

    @staticmethod
    def authenticate_user(username_or_email, password):
        users = Users.load_users()
        for user in users:
            if (user['username'] == username_or_email or user['email'] == username_or_email) and user[
                'password'] == password:
                return True
        return False

    @staticmethod
    def get_username_from_email(email):
        users = Users.load_users()
        for user in users:
            if user['email'] == email:
                return user['username']
        return None

    @staticmethod
    def create_user(user_data):
        users = Users.load_users()
        if any(user['email'] == user_data['email'] for user in users):
            return {'message': 'Email already exists'}, 400
        users.append(user_data)
        Users.save_users(users)
        return user_data, 201

    @staticmethod
    def delete_user(username):
        users = Users.load_users()
        users = [user for user in users if user.get('username') != username]
        Users.save_users(users)
        return {'message': 'User deleted'}, 200

    def is_username_unique(username):
        users = Users.load_users()
        for user in users:
            if user['username'] == username:
                return False
        return True