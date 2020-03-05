from db.models import User


def warn_user(user: User):
    return f'warn {user}'
