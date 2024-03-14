from unittest.mock import create_autospec


from src.core.category.application.use_cases.get_category import (
    CategoryGetRequest,
    CategoryGetResponse,
    GetCategory,
)
from src.core.category.domain.category import Category
from src.core.category.application.category_repository import CategoryRepository


class TestGetCategoryById:
    def test_return_found_category(self):
        category = Category(name="name", description="description", is_active=True)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        use_case = GetCategory(repository=mock_repository)
        response = use_case.execute(request=CategoryGetRequest(id=category.id))

        assert response is not None
        assert response == CategoryGetResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
