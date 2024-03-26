import uuid


from src.core.genre.infra.in_memory_genre import InMemoryGenreRepository

from src.core.category.infra.in_memory_category import InMemoryCategoryRepository

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.create_genre import (
    CreateGenre,
    CreateGenreRequest,
)
from src.core.genre.application.use_cases.exceptions import (
    RelatedCategoriesNotFound,
)


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def category_repository_with_categories(
    movie_category, documentary_category
) -> CategoryRepository:
    return InMemoryCategoryRepository([movie_category, documentary_category])


class TestCreateGenre:
    def test_create_genre_with_associated_categories(
        self,
        documentary_category,
        movie_category,
        category_repository_with_categories,
    ):
        repository = InMemoryGenreRepository()
        repository_category = category_repository_with_categories

        use_case = CreateGenre(
            repository=repository, repository_category=repository_category
        )
        genre = use_case.execute(
            CreateGenreRequest(
                name="Action", categories={movie_category.id, documentary_category.id}
            )
        )

        genre_saved = repository.get_by_id(genre.id)

        assert len(repository.list()) == 1
        assert isinstance(genre.id, uuid.UUID)
        assert genre_saved.name == "Action"
        assert genre_saved.categories == {movie_category.id, documentary_category.id}

    def test_create_genre_with_inexistent_categories_raise_an_error(self):
        repository = InMemoryGenreRepository()
        repository_category = InMemoryCategoryRepository()

        use_case = CreateGenre(
            repository=repository, repository_category=repository_category
        )
        with pytest.raises(RelatedCategoriesNotFound, match="Categories not found:"):
            use_case.execute(
                CreateGenreRequest(name="Action", categories={uuid.uuid4()})
            )

    def test_create_genre_without_categories(self):
        repository = InMemoryGenreRepository()
        repository_category = InMemoryCategoryRepository()

        use_case = CreateGenre(
            repository=repository, repository_category=repository_category
        )
        genre = use_case.execute(CreateGenreRequest(name="Action"))

        genre_saved = repository.get_by_id(genre.id)

        assert len(repository.list()) == 1
        assert isinstance(genre.id, uuid.UUID)
        assert genre_saved.name == "Action"
        assert genre_saved.categories == set()
