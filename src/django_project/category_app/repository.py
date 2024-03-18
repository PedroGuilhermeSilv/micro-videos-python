from uuid import UUID
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from django_project.category_app.models import Category as CategoryModel


class DjangoORMCategoryRespository(CategoryRepository):
    def __init__(self, category_model: CategoryModel):
        self.category_model = category_model

    def save(self, category: Category) -> None:
        if category.id:
            self.category_model.objects.create(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )
        else:
            self.category_model.objects.create(
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )

    def get_by_id(self, id: UUID) -> Category | None:
        if category := self.category_model.objects.filter(id=id).first():
            return Category(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )

    def delete(self, id: UUID) -> None:
        self.category_model.objects.filter(id=id).delete()

    def list(self) -> list[Category] | None:
        return [
            Category(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )
            for category in self.category_model.objects.all()
        ]

    def update(self, category) -> None:
        if old_category := self.get_by_id(category.id):
            self.delete(old_category.id)
            self.save(category)
