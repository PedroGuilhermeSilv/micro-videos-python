from dataclasses import dataclass, field
from uuid import UUID

from src.core.genre.domain.genre import Genre

from src.core.genre.application.genre_repository import GenreRepository

from src.core.genre.application.use_cases.exceptions import (
    InvalidGenre,
    RelatedCategoriesNotFound,
)

from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class CreateGenreRequest:
    name: str
    categories: set[UUID] = field(default_factory=set)
    is_active: bool = True


@dataclass
class CreateGenreResponse:
    id: UUID


class CreateGenre:
    def __init__(
        self, repository: GenreRepository, repository_category: CategoryRepository
    ):
        self.repository = repository
        self.repository_category = repository_category

    def execute(self, request: CreateGenreRequest) -> CreateGenreResponse:
        categories_ids = {category.id for category in self.repository_category.list()}
        if not request.categories.issubset(categories_ids):
            raise RelatedCategoriesNotFound(
                f"Categories not found: {request.categories - categories_ids}"
            )
        try:
            genre = Genre(
                name=request.name,
                is_active=request.is_active,
                categories=request.categories,
            )
            self.repository.save(genre)
        except Exception as err:
            raise InvalidGenre(err) from err
        return CreateGenreResponse(id=genre.id)
