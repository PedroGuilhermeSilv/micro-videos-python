import uuid
from src.core.genre.application.use_cases.exceptions import GenreNotFound
import pytest
from src.core.genre.application.use_cases.delete_genre import (
    DeleteGenre,
    DeleteGenreRequest,
)
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre import InMemoryGenreRepository


class TestDeleteGenre:
    def test_delete_genre_by_id(self):
        genre = Genre(name="Action")
        repository = InMemoryGenreRepository([genre])
        use_case = DeleteGenre(repository=repository)
        response = use_case.execute(request=DeleteGenreRequest(id=genre.id))

        assert repository.list() == []
        assert response is None

    def test_raises_exception_when_genre_does_not_exist(self):
        repository = InMemoryGenreRepository()
        use_case = DeleteGenre(repository=repository)
        id_not_found = uuid.uuid4()

        with pytest.raises(GenreNotFound, match=f"Genre {id_not_found} not found"):
            use_case.execute(request=DeleteGenreRequest(id=id_not_found))
