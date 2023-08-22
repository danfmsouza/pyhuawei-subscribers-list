from config import USERNAME, PASSWORD

class AuthManager:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authenticate(self):
        return self.username == USERNAME and self.password == PASSWORD
