from unittest.mock import MagicMock
from uuid import UUID


from src.core.category.application.category_repository import CategoryRepository
import pytest


from src.core.category.application.use_cases.create_category import (
    CategoryCreateRequest,
    CategoryCreateResponse,
    InvalidCategoryData,
)
from src.core.category.application.use_cases.create_category import CreateCategory


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        mock_repository = MagicMock(CategoryRepository)
        use_case = CreateCategory(repository=mock_repository)
        response = use_case.execute(
            request=CategoryCreateRequest(
                name="name", description="description", is_active=True
            )
        )

        assert response is not None
        assert isinstance(response, CategoryCreateResponse)
        assert isinstance(response.id, UUID)
        assert mock_repository.save.called

    def test_create_category_with_invalid_data(self):
        use_case = CreateCategory(repository=MagicMock(CategoryRepository))
        with pytest.raises(InvalidCategoryData, match="Name is required") as exc_info:
            use_case.execute(request=CategoryCreateRequest(name=""))
        assert exc_info.type == InvalidCategoryData
