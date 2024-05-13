from src.core.category.application.use_cases.create_category import (
    CategoryCreateRequest,
    CategoryCreateResponse,
    CreateCategory,
)
from src.core.category.infra.in_memory_category import InMemoryCategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        response = use_case.execute(
            request=CategoryCreateRequest(
                name="name", description="description", is_active=True
            )
        )

        assert response is not None
        assert isinstance(response, CategoryCreateResponse)
        assert len(repository.categories) == 1

        category = repository.categories[0]
        assert category.name == "name"
        assert category.description == "description"
        assert category.is_active is True
        assert category.id == response.id
