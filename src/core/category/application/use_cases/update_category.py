from dataclasses import dataclass
from uuid import UUID
from core.category.domain.category import Category
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.category_repository import CategoryRepository


@dataclass
class CategoryUpdateRequest:
    id: UUID
    name: str | None = None
    description: str | None = None


class UpdateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: CategoryUpdateRequest) -> None:
        category = self.repository.get_by_id(request.id)
        current_name = category.name
        currrent_description = category.description
        if category is None:
            raise CategoryNotFound(f"Category {request.id} not found")

        if request.name is not None:
            current_name = request.name
        if request.description is not None:
            currrent_description = request.description

        self.repository.update(
            Category(name=current_name, description=currrent_description)
        )
