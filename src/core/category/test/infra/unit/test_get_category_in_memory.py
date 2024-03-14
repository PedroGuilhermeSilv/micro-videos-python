import uuid
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category import InMemoryCategoryRepository


class TestGetCategory:
    def test_can_get_category_by_id(self):
        category = Category(name="name", description="description", is_active=True)
        repository = InMemoryCategoryRepository(categories=[category])
        category_found = repository.get_by_id(category.id)

        assert category_found is not None
        assert category_found == Category(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

    def test_returns_none_when_category_does_not_exist(self):
        repository = InMemoryCategoryRepository()
        id_not_found = uuid.uuid4()
        category_found = repository.get_by_id(id=id_not_found)

        assert category_found is None
