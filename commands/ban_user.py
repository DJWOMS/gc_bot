from db.models import User


def ban_user(user: User):
    return f'Пользователь {user.username} БАН {user.is_banned}'
