from db.models import User


def ban_user(user: User):
    return f'updated {user}'
