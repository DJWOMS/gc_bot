from datetime import datetime

from peewee import (
    SqliteDatabase, Model,
    CharField, DateTimeField,
    ForeignKeyField, IntegerField,
    BooleanField,
)

db = SqliteDatabase('dcgc_channels.db', pragmas={
    'foreign_keys': 1,  # Enforce foreign-key constraints
})


class User(Model):
    """
    User instance will creating from telegram api result message.
    user_id, username, first_name, last_name - this fields getting from telegram api message from user.
    is_sudo. Superuser can send sudo commands to chat.
    """
    telegram_id = IntegerField(unique=True, verbose_name='Telegram id пользователя')
    username = CharField(null=True, verbose_name='Никнейм')
    first_name = CharField(null=True, verbose_name='Имя пользователя')
    last_name = CharField(null=True, verbose_name='Фамилия')
    is_sudo = BooleanField(default=False, verbose_name='Суперпользователь')

    class Meta:
        database = db

    def __repr__(self):
        return f'{self.user_id} {self.username} {self.first_name} {self.last_name} {self.is_sudo} ' \
               f'{self.is_banned} {self.warn}'


class BlackList(Model):
    """Table for banned users"""
    user = ForeignKeyField(User, verbose_name='Пользователь', on_delete='CASCADE')
    datetime_add = DateTimeField(verbose_name='Дата и время добавления', default=datetime.now())
    till_date = DateTimeField(verbose_name='Дата и время снятия бана')

    class Meta:
        database = db


class Warns(Model):
    """Warnings table"""
    user = ForeignKeyField(User, verbose_name='Пользователь')
    warn_number = IntegerField(default=0, verbose_name='Номер предупреждения')
    reason = CharField(verbose_name='Причина предупреждения')
    datetime_add = DateTimeField(verbose_name='Дата и время добавления', default=datetime.now())
    till_date = DateTimeField(verbose_name='Дата и время снятия предупреждения')

    class Meta:
        database = db


def init_db():
    db.create_tables([User, BlackList, Warns], safe=True)


def get_sudoers():
    """Get all sudo users from db"""
    return [user.telegram_id for user in User.select(User.telegram_id).where(User.is_sudo == True)]


def get_warn_users(telegram_id: int) -> str:
    """
    Get warnings user
    :param telegram_id: int: User telegram id
    :return: str: Does not exist or user if exists
    """
    try:
        query = (Warns
                 .select(Warns.warn_number, Warns.reason, Warns.till_date)
                 .join(User, on=(Warns.user_id == User.id))
                 .where(User.telegram_id == telegram_id)).get()
    except Warns.DoesNotExist:
        return '<Model: Warns> instance matching query does not exist'
    return query

