from unittest.mock import create_autospec
import pytest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.category_repository import CategoryRepository
from src.core.category.domain.category import Category

from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    CategoryUpdateRequest,
)


class TestUpdateCategory:
    def test_update_name_category(self):
        category = Category(name="name", description="description", is_active=True)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        use_case.execute(request=CategoryUpdateRequest(id=category.id, name="new name"))

        assert category.name == "new name"
        mock_repository.update.assert_called_once_with(category)
        assert category.description == "description"

    def test_update_description_category(self):
        category = Category(name="name", description="description", is_active=True)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        use_case.execute(
            request=CategoryUpdateRequest(id=category.id, description="new description")
        )

        assert category.description == "new description"
        mock_repository.update.assert_called_once_with(category)
        assert category.name == "name"

    def test_activate_category(self):
        category = Category(name="name", description="description", is_active=False)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        use_case.execute(request=CategoryUpdateRequest(id=category.id, is_active=True))

        assert category.is_active is True
        mock_repository.update.assert_called_once_with(category)
        assert category.name == "name"
        assert category.description == "description"

    def test_deactivate_category(self):
        category = Category(name="name", description="description", is_active=True)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        use_case.execute(request=CategoryUpdateRequest(id=category.id, is_active=False))

        assert category.is_active is False
        mock_repository.update.assert_called_once_with(category)
        assert category.name == "name"
        assert category.description == "description"

    def test_raises_exception_when_category_does_not_exist(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None
        use_case = UpdateCategory(repository=mock_repository)
        id_not_found = "id_not_found"
        request = CategoryUpdateRequest(id=id_not_found)

        with pytest.raises(
            CategoryNotFound, match=f"Category {id_not_found} not found"
        ) as exc_info:
            use_case.execute(request=request)

        assert exc_info.type == CategoryNotFound
        mock_repository.update.assert_not_called()
        mock_repository.get_by_id.assert_called_once_with(id_not_found)

    def test_raises_exception_when_category_name_length_max_255(self):
        category = Category(name="name", description="description", is_active=True)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        use_case = UpdateCategory(repository=mock_repository)
        request = CategoryUpdateRequest(id=category.id, name="a" * 256)

        with pytest.raises(ValueError) as exc_info:
            use_case.execute(request=request)

        assert exc_info.type == ValueError
        assert exc_info.value.args[0] == "Name must have less than 255 characters"
        mock_repository.update.assert_not_called()
        mock_repository.get_by_id.assert_called_once_with(category.id)
