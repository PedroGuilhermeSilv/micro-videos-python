from core.category.application.category_repository import CategoryRepository


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories=None):
        self.categories = categories or []
