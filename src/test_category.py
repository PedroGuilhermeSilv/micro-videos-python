import uuid
from category import Category
import pytest


class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError):
            Category("a" * 256)

    def test_default_values(self):
        category = Category("name")
        assert isinstance(category.id, uuid.UUID)
        assert category.description == ""
        assert category.is_active is True

    def test_str_is_correct(self):
        category = Category("name", "1", "description", True)
        assert str(category) == "Category: name - 1 - description - True"

    def test_repr_is_correct(self):
        category = Category("name", "1", "description", True)
        assert (
            repr(category) == "Category: name - 1 - description - True"
        )

    def test_uuid_is_generated(self):
        category = Category("name")
        assert category.id is not None
        assert isinstance(category.id, uuid.UUID)


class TestUpdateCategory():
    def test_update_category(self):
        category = Category(name='Série', description='Séries de TV')
        category.update_category(name='Filme', description='Filme de TV')

        assert category.name == 'Filme'
        assert category.description == 'Filme de TV'
