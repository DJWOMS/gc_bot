from peewee import (
    SqliteDatabase, Model,
    CharField, DateTimeField,
    ForeignKeyField, IntegerField,
    SmallIntegerField
)


db = SqliteDatabase('dcgc_group.db')


class User(Model):
    """
    User instance will creating from telegram api result message.
    user_id, username, first_name, last_name - this fields getting from telegram api message from user.
    Field warn. If user collect three warnings then his been banned automatically.
    """
    telegram_id = IntegerField(unique=True, verbose_name='Telegram id пользователя')
    username = CharField(null=True, verbose_name='Никнейм')
    first_name = CharField(null=True, verbose_name='Имя пользователя')
    last_name = CharField(null=True, verbose_name='Фамилия')
    warn = SmallIntegerField(verbose_name='Предупреждения')

    class Meta:
        database = db

    def __repr__(self):
        return f'{self.user_id} {self.username} {self.first_name} {self.last_name} {self.is_sudo} ' \
               f'{self.is_banned} {self.warn}'


class Sudo(Model):
    """Table for superusers"""
    user = ForeignKeyField(User, null=True, verbose_name='Пользователь')
    datetime_add = DateTimeField(verbose_name='Дата и время добавления')

    class Meta:
        database = db


class BlackList(Model):
    """Table for banned users"""
    user = ForeignKeyField(User, null=True, verbose_name='Пользователь')
    datetime_add = DateTimeField(verbose_name='Дата и время добавления')

    class Meta:
        database = db


def init_db():
    db.create_tables([User, Sudo, BlackList], safe=True)
