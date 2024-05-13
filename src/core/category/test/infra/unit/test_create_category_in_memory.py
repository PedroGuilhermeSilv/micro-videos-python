from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category import InMemoryCategoryRepository


class TestSave:
    def test_can_save_a_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(name="name", description="description", is_active=True)
        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category
