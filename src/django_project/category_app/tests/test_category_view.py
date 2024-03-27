import json
import uuid

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.category_app.models import Category as CategoryModel
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
class TestListAPI:
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
        assert response.data == {
            "data": [
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
        }
        assert response.status_code == 200

        assert len(response.data["data"]) == 2


@pytest.mark.django_db
class TestRetrieveAPI:
    def test_return_400_when_id_is_invalid(self):
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
            "data": {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active,
            }
        }

    def test_return_404_when_category_not_exists(self):
        response = APIClient().get(f"/api/categories/{uuid.uuid4()}/")

        assert response.status_code == 404


@pytest.mark.django_db
class TestCreateAPI:
    def test_when_payload_is_invalid_then_return_400(self):
        response = APIClient().post(
            "/api/categories/",
            data={
                "name": "",
                "description": "description",
                "is_active": True,
            },
        )

        assert response.status_code == 400
        assert response.data == {"name": ["This field may not be blank."]}

    def test_return_201_when_payload_is_valid(
        self, category_repository: DjangoORMCategoryRepository
    ):
        response = APIClient().post(
            "/api/categories/",
            data={
                "name": "Category 1",
                "description": "Description 1",
                "is_active": True,
            },
        )

        assert response.status_code == 201
        assert response.data == {
            "id": response.data["id"],
        }


@pytest.mark.django_db
class TestUpdatedAPI:
    def test_return_400_when_id_is_invalid(
        self,
        category_repository: DjangoORMCategoryRepository,
    ):
        response = APIClient().put(
            "/api/categories/1/",
            content_type="application/json",
            data=json.dumps(
                {"name": "Category", "description": "asdf", "is_active": False}
            ),
        )

        assert response.status_code == 400
        assert response.data == {"id": ["Must be a valid UUID."]}

    def test_return_404_when_category_not_exists(
        self,
        category_repository: DjangoORMCategoryRepository,
    ):
        response = APIClient().put(
            f"/api/categories/{uuid.uuid4()}/",
            content_type="application/json",
            data=json.dumps(
                {"name": "Category", "description": "asdf", "is_active": False}
            ),
        )

        assert response.status_code == 404
        assert response.data == "Category not found"

    def test_return_400_when_payload_is_invalid(
        self, category_repository: DjangoORMCategoryRepository
    ):
        response = APIClient().put(
            f"/api/categories/{uuid.uuid4()}/",
            content_type="application/json",
            data=json.dumps({"name": "", "description": "asdf", "is_active": False}),
        )

        assert response.status_code == 400
        assert response.data == {"name": ["This field may not be blank."]}

    def test_return_204_when_payload_is_valid(
        self, category_movie: Category, category_repository: DjangoORMCategoryRepository
    ):
        repository = category_repository
        repository.save(category_movie)

        old_category = repository.get_by_id(category_movie.id)
        assert old_category.name == "Category 1"
        assert old_category.description == "Description 1"
        assert old_category.is_active is True

        response = APIClient().put(
            f"/api/categories/{category_movie.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": "Category update",
                    "description": "Description updated",
                    "is_active": False,
                }
            ),
        )

        assert response.status_code == 204
        assert response.data == "Category updated successfully"

        updated_category = repository.get_by_id(category_movie.id)
        assert updated_category.name == "Category update"
        assert updated_category.description == "Description updated"
        assert updated_category.is_active is False


@pytest.mark.django_db
class TestDeleteAPI:
    def test_return_204_when_category_exists(
        self, category_movie: Category, category_repository: DjangoORMCategoryRepository
    ):
        repository = category_repository
        repository.save(category_movie)

        assert CategoryModel.objects.count() == 1

        response = APIClient().delete(f"/api/categories/{category_movie.id}/")

        assert response.status_code == 204
        assert response.data == "Category deleted successfully"
        assert CategoryModel.objects.count() == 0

    def test_return_404_when_category_not_exists(self):
        response = APIClient().delete(
            f"/api/categories/{uuid.uuid4()}/",
            content_type="application/json",
            data=json.dumps(
                {"name": "Category", "description": "asdf", "is_active": False}
            ),
        )

        assert response.status_code == 404
        assert response.data == "Category not found"

    def test_return_400_when_id_is_invalid(self):
        response = APIClient().delete("/api/categories/1/")

        assert response.status_code == 400
        assert response.data == {"id": ["Must be a valid UUID."]}
