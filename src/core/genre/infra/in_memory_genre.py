from uuid import UUID

from src.core.genre.domain.genre import Genre
from src.core.genre.application.genre_repository import GenreRepository


class InMemoryGenreRepository(GenreRepository):
    def __init__(self, genres=None):
        self.genres = genres or []

    def save(self, genre: Genre):
        self.genres.append(genre)

    def get_by_id(self, id: UUID) -> Genre | None:
        return next((genre for genre in self.genres if genre.id == id), None)

    def delete(self, id: UUID) -> None:
        self.genres.remove(self.get_by_id(id))

    def update(self, genre: Genre) -> None:
        if old_genre := self.get_by_id(genre.id):
            self.genres.remove(old_genre)
            self.genres.append(genre)

    def list(self) -> list[Genre]:
        return list(self.genres)
