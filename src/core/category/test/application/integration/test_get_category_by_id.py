import uuid
from src.core.category.application.use_cases.exceptions import CategoryNotFound
import pytest
from src.core.category.application.use_cases.get_category import (
    CategoryGetRequest,
    CategoryGetResponse,
    GetCategory,
)
from src.core.category.infra.in_memory_category import InMemoryCategoryRepository
from src.core.category.domain.category import Category


class TestGetCategoryById:
    def test_get_category_by_id(self):
        category_movie = Category(name="movie", description="movie description")

        category_series = Category(name="series", description="series description")

        repository = InMemoryCategoryRepository(
            categories=[category_movie, category_series]
        )
        use_case = GetCategory(repository=repository)
        request = CategoryGetRequest(id=category_movie.id)
        response = use_case.execute(request=request)

        assert isinstance(response, CategoryGetResponse)

        assert response is not None
        assert response == CategoryGetResponse(
            id=category_movie.id,
            name=category_movie.name,
            description=category_movie.description,
            is_active=category_movie.is_active,
        )

    def test_raises_exception_when_category_does_not_exist(self):
        repository = InMemoryCategoryRepository()
        use_case = GetCategory(repository=repository)
        id_not_found = uuid.uuid4()
        request = CategoryGetRequest(id=id_not_found)

        with pytest.raises(
            CategoryNotFound, match=f"Category {id_not_found} not found"
        ) as exc_info:
            use_case.execute(request=request)

        assert exc_info.type == CategoryNotFound
