from dataclasses import dataclass
from uuid import UUID
from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import InvalidCategoryData
from src.core.category.domain.category import Category


@dataclass
class CategoryCreateRequest:
    name: str
    description: str = ""
    is_active: bool = True


@dataclass
class CategoryCreateResponse:
    id: UUID


class CreateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: CategoryCreateRequest) -> CategoryCreateResponse:
        try:
            category = Category(
                name=request.name,
                description=request.description,
                is_active=request.is_active,
            )
            category.validate()
        except ValueError as err:
            raise InvalidCategoryData(str(err)) from err
        self.repository.save(category)
        return CategoryCreateResponse(id=category.id)
