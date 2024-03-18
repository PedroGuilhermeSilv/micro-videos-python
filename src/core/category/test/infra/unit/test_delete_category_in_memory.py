from unittest.mock import create_autospec
import uuid

from src.core.category.application.use_cases.exceptions import CategoryNotFound
import pytest
from core.category.domain.category_repository import CategoryRepository
from src.core.category.domain.category import Category
from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category = Category(name="name", description="description", is_active=True)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = DeleteCategory(mock_repository)
        use_case.execute(DeleteCategoryRequest(id=category.id))

        mock_repository.delete.assert_called_once_with(
            category.id
        )  # Ensures that the delete method was called with the category ID.

    def test_raises_exception_when_category_not_found(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None
        id_not_found = uuid.uuid4()

        use_case = DeleteCategory(mock_repository)
        with pytest.raises(
            CategoryNotFound, match=f"Category {id_not_found} not found"
        ):
            use_case.execute(DeleteCategoryRequest(id=id_not_found))

        mock_repository.delete.assert_not_called()
