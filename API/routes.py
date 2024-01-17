from flask import Blueprint, request, jsonify
import json
import os

api_blueprint = Blueprint('api', __name__)

USERS_FILE = os.path.join('api', 'users.json')

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r') as file:
        return json.load(file)

def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)


def authenticate_user(username_or_email, password):
    users = load_users()
    for user in users:
        if (user['username'] == username_or_email or user['email'] == username_or_email) and user['password'] == password:
            return True
    return False


def get_username_from_email(email):
    users = load_users()
    for user in users:
        if user['email'] == email:
            return user['username']
    return None  # or handle the case where the email is not found


@api_blueprint.route('/users', methods=['POST'])
def create_user(user_data):
    users = load_users()

    if any(user['username'] == user_data['username'] for user in users):
        return jsonify({'message': 'Username already exists'}), 400

    users.append(user_data)
    save_users(users)
    return jsonify(user_data), 201

@api_blueprint.route('/users/<string:username>', methods=['DELETE'])
def delete_user(username):
    users = load_users()
    users = [user for user in users if user.get('username') != username]
    save_users(users)
    return jsonify({'message': 'User deleted'}), 200

