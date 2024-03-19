import uuid
from src.core.category.domain.category import Category
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.models import Category as CategoryModel
from rest_framework.test import APIClient
import pytest


@pytest.fixture
def category_movie() -> Category:
    return Category(name="Category 1", description="Description 1", is_active=True)


@pytest.fixture
def category_serie() -> Category:
    return Category(name="Category 2", description="Description 2", is_active=False)


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository(CategoryModel)


@pytest.mark.django_db
class TestCategoryAPI:
    def test_list_category(
        self,
        category_movie: Category,
        category_serie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        repository = category_repository
        repository.save(category_serie)
        repository.save(category_movie)

        response = APIClient().get("/api/categories/")
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
        assert response.status_code == 200
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


@pytest.mark.django_db
class TestRetrieveAPI:

    def test_return_400_when_id_is_invalid(
        self,
        category_repository: DjangoORMCategoryRepository,
    ):
        response = APIClient().get("/api/categories/1/")

        assert response.status_code == 400

    def test_return_category_when_exists(
        self,
        category_movie: Category,
        category_serie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        repository = category_repository
        repository.save(category_movie)
        repository.save(category_serie)

        response = APIClient().get(f"/api/categories/{category_movie.id}/")

        assert response.status_code == 200
        assert response.data == {
            "id": str(category_movie.id),
            "name": category_movie.name,
            "description": category_movie.description,
            "is_active": category_movie.is_active,
        }

    def test_return_404_when_category_not_exists(
        self,
        category_repository: DjangoORMCategoryRepository,
    ):
        response = APIClient().get(f"/api/categories/{uuid.uuid4()}/")

        assert response.status_code == 404
