from dataclasses import dataclass
from uuid import UUID
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from core.category.domain.category_repository import CategoryRepository


@dataclass
class CategoryUpdateRequest:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class UpdateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: CategoryUpdateRequest) -> None:
        category = self.repository.get_by_id(request.id)
        if category is None:
            raise CategoryNotFound(f"Category {request.id} not found")

        current_name = category.name
        if request.name is not None:
            current_name = request.name
        current_description = category.description
        if request.description is not None:
            current_description = request.description

        category.update_category(name=current_name, description=current_description)

        if request.is_active is True:
            category.activate()
        elif request.is_active is False:
            category.deactivate()

        category.validate()

        self.repository.update(category)
