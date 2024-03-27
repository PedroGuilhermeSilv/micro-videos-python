from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository

from src.core.genre.application.genre_repository import GenreRepository
from src.core.genre.application.use_cases.exceptions import (
    GenreNotFound,
    RelatedCategoriesNotFound,
)
from src.core.genre.domain.genre import Genre


@dataclass
class GenreUpdateRequest:
    id: UUID
    name: str
    is_active: bool
    categories: set[UUID] | None = None


class UpdateGenre:
    def __init__(
        self, repository: GenreRepository, repository_category: CategoryRepository
    ):
        self.repository = repository
        self.repository_category = repository_category

    def execute(self, request: GenreUpdateRequest) -> None:
        genre = self.repository.get_by_id(request.id)
        if genre is None:
            raise GenreNotFound(f"Genre {request.id} not found")
        if request.categories:
            categories_ids = {
                category.id for category in self.repository_category.list()
            }
            if not request.categories.issubset(categories_ids):
                raise RelatedCategoriesNotFound(
                    f"Categories not found: {request.categories - categories_ids}"
                )

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
