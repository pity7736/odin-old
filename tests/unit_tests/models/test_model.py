import datetime

from pytest import raises

from src.db.models import Model
from src.db.fields import Field


class ChildModel(Model):
    __table_name__ = 'Test model'
    id = Field(name='id')
    name = Field(name='name')
    date = Field(name='date')


def test_correct_fields():
    child_model = ChildModel(id=1, name='hi', date=datetime.date.today())

    assert child_model.id == 1
    assert child_model.name == 'hi'
    assert child_model.date == datetime.date.today()


def test_wrong_fields():
    with raises(TypeError):
        ChildModel(id=1, name='hi', dated=datetime.date.today())


def test_instantiate_with_only_name():
    instance = ChildModel(name='hi')

    assert instance.name == 'hi'
    assert instance.id is None
    assert instance.date is None


def test_model_must_have_a_table_name():
    with raises(AssertionError):
        class M(Model):
            pass
