class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def get_username(self):
        return self.username

    def update_username(self, new_username, users):
        if users.is_username_unique(new_username):
            self.username = new_username
            users.update_user_data(self)
            return True
        else:
            return False
