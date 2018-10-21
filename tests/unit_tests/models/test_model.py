import datetime

from pytest import raises

from src.db.models import Model
from src.db.fields import Field, ForeignKeyField


class Model1(Model):
    __table_name__ = 'test_model'
    id = Field(name='id')
    name = Field(name='name')
    date = Field(name='date')


class Model2(Model):
    __table_name__ = 'test'
    id = Field(name='id')
    model1 = ForeignKeyField(name='model1', to=Model1)


def test_correct_fields():
    child_model = Model1(id=1, name='hi', date=datetime.date.today())

    assert child_model.id == 1
    assert child_model.name == 'hi'
    assert child_model.date == datetime.date.today()


def test_wrong_fields():
    with raises(TypeError):
        Model1(id=1, name='hi', dated=datetime.date.today())


def test_instantiate_with_only_name():
    instance = Model1(name='hi')

    assert instance.name == 'hi'
    assert instance.id is None
    assert instance.date is None


def test_model_must_have_a_table_name():
    with raises(AssertionError):
        class M(Model):
            pass


def test_model_foreign_key():
    model2 = Model2()

    assert model2.model1 is None
    assert model2.model1_id is None


def test_model_foreign_key_with_id():
    model2 = Model2(model1_id=1)

    assert model2.model1_id == 1
