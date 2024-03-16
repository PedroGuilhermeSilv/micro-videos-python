from src.core.category.infra.in_memory_category import InMemoryCategoryRepository
from src.core.category.domain.category import Category

from src.core.category.application.use_cases.list_category import (
    CategoryOutput,
    ListCategory,
    ListCategoryRequest,
    ListCategoryResponse,
)


class TestListCategory:
    def test_when_list_category_is_empty(self):
        repository = InMemoryCategoryRepository()
        use_case = ListCategory(repository=repository)
        response = use_case.execute(request=ListCategoryRequest())

        assert response == ListCategoryResponse(data=[])

    def test_when_list_category_has_one_category(self):
        category_movie = Category(name="movie", description="description")
        category_series = Category(name="series", description="description")

        repository = InMemoryCategoryRepository()
        repository.save(category_movie)
        repository.save(category_series)
        use_case = ListCategory(repository=repository)
        response = use_case.execute(request=ListCategoryRequest())

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category_movie.id,
                    name=category_movie.name,
                    description=category_movie.description,
                    is_active=category_movie.is_active,
                ),
                CategoryOutput(
                    id=category_series.id,
                    name=category_series.name,
                    description=category_series.description,
                    is_active=category_series.is_active,
                ),
            ]
        )
