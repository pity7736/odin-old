from pytest import raises

from src.db.fields import Field


def test_field_attributes():
    field = Field(name='test_name')

    assert field.name == 'test_name'


def test_validate_name():
    with raises(ValueError, match='test name is a invalid name field'):
        Field(name='test name')
