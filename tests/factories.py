import datetime

import factory

from odin.accounting.models import Category, Movement, Tag, Wallet, Event
from odin.auth.models import User


class CategoryFactory(factory.Factory):
    id = factory.Sequence(lambda n: n)
    name = 'test name'
    description = 'test description'

    class Meta:
        model = Category


class TagFactory(factory.Factory):
    name = 'test tag'

    class Meta:
        model = Tag


class WalletFactory(factory.Factory):
    id = factory.Sequence(lambda n: n)
    name = 'test wallet'
    initial_balance = 5_000_000
    balance = 5_000_000
    created = factory.LazyFunction(datetime.datetime.now)

    class Meta:
        model = Wallet


class EventFactory(factory.Factory):
    id = factory.Sequence(lambda n: n)
    name = 'test event'
    init_date = factory.LazyFunction(datetime.datetime.now)
    end_date = factory.LazyAttribute(lambda e: e.init_date + datetime.timedelta(days=2))

    class Meta:
        model = Event


class MovementFactory(factory.Factory):
    type = 'expense'
    date = factory.LazyFunction(datetime.date.today)
    value = 10000
    note = 'note'

    class Meta:
        model = Movement


class UserFactory(factory.Factory):
    email = factory.Faker('email')
    password = factory.Faker('password')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    created = factory.LazyFunction(datetime.datetime.now)

    class Meta:
        model = User
