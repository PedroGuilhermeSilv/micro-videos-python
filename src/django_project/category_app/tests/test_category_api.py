from src.core.category.domain.category import Category
from rest_framework.test import APITestCase
from django_project.category_app.repository import DjangoORMCategoryRespository
from django_project.category_app.models import Category as CategoryModel


class TestCategoryAPI(APITestCase):
    def test_list_category(self):
        category_movie = Category(
            name="Category 1", description="Description 1", is_active=True
        )
        category_serie = Category(
            name="Category 2", description="Description 2", is_active=False
        )

        repository = DjangoORMCategoryRespository(CategoryModel)
        repository.save(category_serie)
        repository.save(category_movie)

        response = self.client.get("/api/categories/")
        assert response.data == [
            {
                "id": str(category_serie.id),
                "name": category_serie.name,
                "description": category_serie.description,
                "is_active": category_serie.is_active,
            },
            {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active,
            },
        ]
        self.assertEqual(response.status_code, 200)
