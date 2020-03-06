class User:
    is_sudo = False
    is_banned = False
    warn = 0

    def __init__(self, user_id, username, first_name, last_name):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def admin(self):
        return self.is_sudo

    def __repr__(self):
        return f'{self.user_id} {self.username} {self.first_name} {self.last_name} {self.is_sudo} {self.is_banned} {self.warn}'
