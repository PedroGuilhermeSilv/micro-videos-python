import uuid
from unittest.mock import create_autospec

from src.core.genre.application.use_cases.list_genre import ListGenreResponse
from src.core.genre.domain.genre import Genre

from src.core.genre.application.genre_repository import GenreRepository

import pytest


@pytest.fixture
def mock_empty_genre_repository() -> GenreRepository:
    repository = create_autospec(GenreRepository)
    repository.list.return_value = ListGenreResponse(data=[])
    return repository


class TestListGenre:
    def test_when_list_genre_is_empty(
        self,
        mock_empty_genre_repository,
    ):
        repository = mock_empty_genre_repository
        response = repository.list()

        assert response == ListGenreResponse(data=[])

    def test_when_list_genre_has_not_category(
        self,
    ) -> None:
        repository = create_autospec(GenreRepository)
        genre = Genre(
            id=uuid.uuid4(),
            name="Action",
        )
        repository.list.return_value = ListGenreResponse(data=[genre])
        response = repository.list()

        assert response == ListGenreResponse(data=[genre])
