import uuid
from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from src.core.category.application.use_cases.exceptions import CategoryNotFound
import pytest

from src.core.category.infra.in_memory_category import InMemoryCategoryRepository
from src.core.category.domain.category import Category


class TestDeleteCategory:
    def test_delete_category_by_id(self):
        category_movie = Category(name="movie", description="movie description")

        category_series = Category(name="series", description="series description")

        repository = InMemoryCategoryRepository(
            categories=[category_movie, category_series]
        )
        use_case = DeleteCategory(repository=repository)
        request = DeleteCategoryRequest(id=category_movie.id)
        response = use_case.execute(request=request)

        assert response is None
        assert len(repository.categories) == 1

    def test_raises_exception_when_category_does_not_exist(self):
        repository = InMemoryCategoryRepository()
        use_case = DeleteCategory(repository=repository)
        id_not_found = uuid.uuid4()
        request = DeleteCategoryRequest(id=id_not_found)

        with pytest.raises(
            CategoryNotFound, match=f"Category {id_not_found} not found"
        ) as exc_info:
            use_case.execute(request=request)

        assert exc_info.type == CategoryNotFound
