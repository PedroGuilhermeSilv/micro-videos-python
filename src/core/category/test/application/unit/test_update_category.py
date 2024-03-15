from unittest.mock import create_autospec
from src.core.category.application.category_repository import CategoryRepository
from src.core.category.domain.category import Category

from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    CategoryUpdateRequest,
)


class TestUpdatecategory:
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
