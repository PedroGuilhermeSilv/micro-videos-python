from dataclasses import dataclass
from uuid import UUID

from src.core.genre.application.genre_repository import GenreRepository
from src.core.genre.application.use_cases.exceptions import GenreNotFound


@dataclass
class DeleteGenreRequest:
    id: UUID


class DeleteGenre:
    def __init__(self, repository: GenreRepository):
        self.repository = repository

    def execute(self, request: DeleteGenreRequest) -> None:
        genre = self.repository.get_by_id(request.id)
        if genre is None:
            raise GenreNotFound(f"Genre {request.id} not found")
        self.repository.delete(genre.id)
