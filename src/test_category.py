import uuid
from category import Category
import pytest


class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument"):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="Name must have less than 255 characters"):
            Category("a" * 256)

    def test_default_values(self):
        category = Category("name")
        assert isinstance(category.id, uuid.UUID)
        assert category.description == ""
        assert category.is_active is True

    def test_create_category_with_all_values(self):
        category = Category("name", "1", "description", True)
        assert category.name == "name"
        assert category.id == "1"
        assert category.description == "description"
        assert category.is_active is True

    def test_cannot_create_category_with_name_empty(self):
        with pytest.raises(ValueError, match="Name is required"):
            Category("")

    def test_str_is_correct(self):
        category = Category("name", "1", "description", True)
        assert str(category) == "Category: name - 1 - description - True"

    def test_repr_is_correct(self):
        category = Category("name", "1", "description", True)
        assert repr(category) == "Category: name - 1 - description - True"

    def test_uuid_is_generated(self):
        category = Category("name")
        assert category.id is not None
        assert isinstance(category.id, uuid.UUID)


class TestUpdateCategory:
    def test_update_category_with_name_and_description(self):
        category = Category(name="Série", description="Séries de TV")
        category.update_category(name="Filme", description="Filme de TV")

        assert category.name == "Filme"
        assert category.description == "Filme de TV"

    def test_update_category_with_name_invalid(self):
        category = Category(name="Série", description="Séries de TV")
        with pytest.raises(ValueError, match="Name must have less than 255 characters"):
            category.update_category(name="a" * 256, description="Filme de TV")

    def test_update_category_with_name_empty(self):
        category = Category(name="Série", description="Séries de TV")
        with pytest.raises(ValueError, match="Name is required"):
            category.update_category(name="", description="Filme de TV")


class TestActiveCategory:
    def test_active_category_inactive(self):
        category = Category(name="Série", description="Séries de TV", is_active=False)
        category.activate()
        assert category.is_active is True

    def test_active_category_active(self):
        category = Category(name="Série", description="Séries de TV")
        category.activate()
        assert category.is_active is True


class TestDeactivateCategory:
    def test_deactivate_category_active(self):
        category = Category(name="Série", description="Séries de TV")
        category.deactivate()
        assert category.is_active is False

    def test_deactivate_category_inactive(self):
        category = Category(name="Série", description="Séries de TV", is_active=False)
        category.deactivate()
        assert category.is_active is False


class TestEquality:
    def test_category_id_equals(self):
        common_id = uuid.uuid4()
        category1 = Category(name="Série", id=common_id)
        category2 = Category(name="Série", id=common_id)
        assert category1 == category2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        category = Category(name="Série", id=common_id)
        dummy = Dummy()
        dummy.id = common_id
        with pytest.raises(ValueError, match="Comparison between different classes"):
            category == dummy
