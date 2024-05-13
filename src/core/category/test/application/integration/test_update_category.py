from src.core.category.application.use_cases.update_category import (
    CategoryUpdateRequest,
    UpdateCategory,
)
from src.core.category.infra.in_memory_category import InMemoryCategoryRepository
from src.core.category.domain.category import Category


class TestUpdateCategory:
    def test_can_update_name_category(self):
        category = Category(name="name", description="description", is_active=True)
        repository = InMemoryCategoryRepository(categories=[category])

        use_case = UpdateCategory(repository=repository)
        use_case.execute(request=CategoryUpdateRequest(id=category.id, name="new name"))

        category.update_category(name="new name", description="description")

        update_category = repository.get_by_id(category.id)
        assert update_category.name == "new name"
        assert update_category.description == "description"

    def test_can_update_description_category(self):
        category = Category(name="name", description="description", is_active=True)
        repository = InMemoryCategoryRepository(categories=[category])

        use_case = UpdateCategory(repository=repository)
        use_case.execute(
            request=CategoryUpdateRequest(id=category.id, description="new description")
        )

        category.update_category(name="name", description="new description")

        update_category = repository.get_by_id(category.id)
        assert update_category.description == "new description"
        assert update_category.name == "name"
