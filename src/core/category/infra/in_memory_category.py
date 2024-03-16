from uuid import UUID

from src.core.category.domain.category import Category
from src.core.category.application.category_repository import CategoryRepository


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories=None):
        self.categories = categories or []

    def save(self, category):
        self.categories.append(category)

    def get_by_id(self, id: UUID) -> Category | None:
        return next(
            (category for category in self.categories if category.id == id), None
        )

    def delete(self, id: UUID) -> None:
        self.categories.remove(self.get_by_id(id))

    def update(self, category: Category) -> None:
        if old_category := self.get_by_id(category.id):
            self.categories.remove(old_category)
            self.categories.append(category)

    def list(self) -> list[Category]:
        return list(self.categories)
