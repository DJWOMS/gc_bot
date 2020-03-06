from db.models import User


def ban_user(username: str, user: User, reason: str):
    return f'{username} забанил пользавателя {user.username}\nПричина: {reason}'
