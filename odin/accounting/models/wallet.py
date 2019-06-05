from gideon.fields import CharField, DateField, IntegerField
from gideon.models import Model


class Wallet(Model):
    __table_name__ = 'wallets'
    _name = CharField(name='name')
    _initial_balance = IntegerField(name='initial_balance')
    _balance = IntegerField(name='balance')
    _created = DateField(name='created')
