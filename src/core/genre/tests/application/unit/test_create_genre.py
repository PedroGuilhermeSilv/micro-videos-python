import uuid
from unittest.mock import create_autospec

from src.core.genre.domain.genre import Genre

from src.core.genre.application.genre_repository import GenreRepository

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.create_genre import (
    CreateGenre,
    CreateGenreRequest,
)
from src.core.genre.application.use_cases.exceptions import (
    InvalidGenre,
    RelatedCategoriesNotFound,
)


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def mock_category_repository_with_categories(
    movie_category, documentary_category
) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository


@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository


class TestCreateGenre:
    def test_when_provided_categories_do_not_exist_then_raise_related_categories_not_found(
        self,
        mock_empty_category_repository,
        mock_genre_repository,
    ):
        repository = mock_genre_repository
        repository_category = mock_empty_category_repository

        category_id_not_found = uuid.uuid4()
        use_case = CreateGenre(
            repository=repository, repository_category=repository_category
        )
        with pytest.raises(RelatedCategoriesNotFound) as err:
            use_case.execute(
                CreateGenreRequest(name="Action", categories={category_id_not_found})
            )
        assert str(category_id_not_found) in str(err.value)

    def test_when_created_genre_is_invalid_then_raise_invalid_genre(
        self,
        movie_category,
        mock_category_repository_with_categories,
        mock_genre_repository,
    ) -> None:
        respository = mock_genre_repository
        repository_category = mock_category_repository_with_categories

        use_case = CreateGenre(
            repository=respository, repository_category=repository_category
        )
        with pytest.raises(InvalidGenre, match="Name is required"):
            use_case.execute(
                CreateGenreRequest(name="", categories={movie_category.id})
            )

    def test_when_created_genre_is_valid_and_categories_exist_then_save_genre(
        self,
        documentary_category,
        movie_category,
        mock_category_repository_with_categories,
        mock_genre_repository,
    ):
        respository = mock_genre_repository
        repository_category = mock_category_repository_with_categories

        use_case = CreateGenre(
            repository=respository, repository_category=repository_category
        )
        response = use_case.execute(
            CreateGenreRequest(
                name="Action", categories={movie_category.id, documentary_category.id}
            )
        )

        assert isinstance(response.id, uuid.UUID)
        respository.save.assert_called_with(
            Genre(
                id=response.id,
                name="Action",
                categories={movie_category.id, documentary_category.id},
            )
        )

    def test_create_genre_without_categories(
        self,
        mock_genre_repository,
        mock_category_repository_with_categories,
    ):
        respository = mock_genre_repository
        repository_category = mock_category_repository_with_categories

        use_case = CreateGenre(
            repository=respository, repository_category=repository_category
        )
        response = use_case.execute(CreateGenreRequest(name="Action"))

        assert isinstance(response.id, uuid.UUID)
        respository.save.assert_called_with(
            Genre(
                id=response.id,
                name="Action",
            )
        )
