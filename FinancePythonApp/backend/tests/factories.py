import factory
from app import db
from app.models import User, Transaction
from werkzeug.security import generate_password_hash


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n + 1)
    username = factory.Sequence(lambda n: f'user_{n}')
    password_hash = factory.LazyFunction(
        lambda: generate_password_hash('password123')
    )


class TransactionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Transaction
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n + 1)
    user_id = 1
    type = 'expense'
    amount = 1500.00
    category = 'Еда'
    description = 'Тестовая транзакция'
    