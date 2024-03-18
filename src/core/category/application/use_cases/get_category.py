from dataclasses import dataclass
from uuid import UUID
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from core.category.domain.category_repository import CategoryRepository


@dataclass
class CategoryGetResponse:
    id: UUID
    name: str
    description: str
    is_active: bool


@dataclass
class CategoryGetRequest:
    id: UUID


class GetCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: CategoryGetRequest) -> CategoryGetResponse:
        category = self.repository.get_by_id(request.id)
        if category is None:
            raise CategoryNotFound(f"Category {request.id} not found")
        return CategoryGetResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
