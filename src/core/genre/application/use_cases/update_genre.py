from dataclasses import dataclass
from uuid import UUID

from src.core.genre.application.genre_repository import GenreRepository
from src.core.genre.application.use_cases.exceptions import GenreNotFound
from src.core.genre.domain.genre import Genre


@dataclass
class GenreUpdateRequest:
    id: UUID
    name: str | None = None
    is_active: bool | None = None
    categories: set[UUID] | None = None


class UpdateGenre:
    def __init__(self, repository: GenreRepository):
        self.repository = repository

    def execute(self, request: GenreUpdateRequest) -> None:
        genre = self.repository.get_by_id(request.id)
        if genre is None:
            raise GenreNotFound(f"Genre {request.id} not found")

        Genre(
            name=request.name if request.name is not None else genre.name,
            is_active=request.is_active
            if request.is_active is not None
            else genre.is_active,
            categories=request.categories
            if request.categories is not None
            else genre.categories,
        )

        self.repository.update(genre)
