
from dataclasses import dataclass
from uuid import UUID
from src.core.genre.application.genre_repository import GenreRepository


@dataclass
class GenreResponse:
    id: UUID
    name: str
    is_active: bool
    categories: set[UUID]


@dataclass
class ListGenreResponse:
    data: list[GenreResponse]


class ListGenre:
    def __init__(self, repository: GenreRepository):
        self.repository = repository

    def execute(self) -> ListGenreResponse:
        genres = self.repository.list()
        return ListGenreResponse(
            data=[
                GenreResponse(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories=genre.categories,
                )
                for genre in genres
            ]
        )

    