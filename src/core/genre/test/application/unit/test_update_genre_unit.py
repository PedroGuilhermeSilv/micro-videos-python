import re
from unittest.mock import create_autospec
import uuid

from src.core.category.infra.in_memory_category import InMemoryCategoryRepository
from src.core.genre.application.genre_repository import GenreRepository
from src.core.genre.application.use_cases.update_genre import (
    GenreUpdateRequest,
    UpdateGenre,
)
from src.core.genre.application.use_cases.exceptions import (
    GenreNotFound,
    RelatedCategoriesNotFound,
)
import pytest
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre import InMemoryGenreRepository


class TestUpdateGenre:
    def test_update_genre_by_id(self):
        mock_repository = create_autospec(InMemoryGenreRepository)
        mock_repository_category = create_autospec(InMemoryCategoryRepository)
        genre = Genre(name="Action")
        mock_repository.get_by_id.return_value = genre
        use_case = UpdateGenre(
            repository=mock_repository, repository_category=mock_repository_category
        )
        use_case.execute(request=GenreUpdateRequest(**genre.__dict__))

        assert mock_repository.update.called
        assert mock_repository.get_by_id.called

    def test_raises_exception_when_genre_does_not_exist(self):
        mock_repository = create_autospec(GenreRepository)
        mock_repository_category = create_autospec(InMemoryCategoryRepository)
        genre = Genre(name="Action")
        mock_repository.get_by_id.return_value = None
        use_case = UpdateGenre(
            repository=mock_repository, repository_category=mock_repository_category
        )
        with pytest.raises(GenreNotFound, match=f"Genre {genre.id} not found"):
            use_case.execute(request=GenreUpdateRequest(**genre.__dict__))

        mock_repository.update.assert_not_called()

    def test_raises_exception_when_categories_do_not_exist(self):
        mock_repository = create_autospec(InMemoryGenreRepository)
        mock_repository_category = create_autospec(InMemoryCategoryRepository)
        genre = Genre(name="Action", categories={uuid.uuid4()})
        mock_repository.get_by_id.return_value = genre
        mock_repository_category.list.return_value = []
        use_case = UpdateGenre(
            repository=mock_repository, repository_category=mock_repository_category
        )
        with pytest.raises(
            RelatedCategoriesNotFound,
            match=re.escape(f"Categories not found: {genre.categories}"),
        ):
            use_case.execute(request=GenreUpdateRequest(**genre.__dict__))

        mock_repository.update.assert_not_called()
