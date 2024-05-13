import json
import uuid
from rest_framework import status
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.category_app.models import Category as CategoryModel
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.models import Genre as GenreModel
from src.core.genre.domain.genre import Genre
from src.core.category.domain.category import Category
from rest_framework.test import APIClient
import pytest


@pytest.fixture
def category_documentary() -> Category:
    return Category(name="Documentary", is_active=True)


@pytest.fixture
def category_movie() -> Category:
    return Category(name="Movie", is_active=True)


@pytest.fixture
def category_repository(
    category_documentary, category_movie
) -> DjangoORMCategoryRepository:
    repository = DjangoORMCategoryRepository(CategoryModel)
    repository.save(category_documentary)
    repository.save(category_movie)
    return repository


@pytest.fixture
def genre_romance(category_movie, category_documentary) -> Genre:
    return Genre(
        name="Romance",
        is_active=True,
        categories={category_movie.id, category_documentary.id},
    )


@pytest.fixture
def genre_drama() -> Genre:
    return Genre(name="Drama", is_active=True, categories={})


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository(GenreModel)


@pytest.mark.django_db
class TestListAPI:
    def test_list_genre_and_categories(
        self,
        genre_romance,
        genre_drama,
        genre_repository,
        category_documentary,
        category_movie,
        category_repository,
    ):
        genre_repository.save(genre_romance)
        genre_repository.save(genre_drama)

        url = "/api/genres/"

        client = APIClient()

        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK

        # expected_response = {
        #     "data": [
        #         {
        #             "id": str(genre_romance.id),
        #             "name": genre_romance.name,
        #             "is_active": genre_romance.is_active,
        #             "categories": [
        #                 str(category_documentary.id),
        #                 str(category_movie.id),
        #             ],
        #         },
        #         {
        #             "id": str(genre_drama.id),
        #             "name": genre_drama.name,
        #             "is_active": genre_drama.is_active,
        #             "categories": [],
        #         },
        #     ]
        # }
        # assert response.data == expected_response

        assert response.data["data"][0]["id"] == str(genre_romance.id)
        assert response.data["data"][0]["name"] == genre_romance.name
        assert response.data["data"][0]["is_active"] == genre_romance.is_active
        assert response.data["data"][0]["categories"] == [
            str(category_movie.id),
            str(category_documentary.id),
        ]

        assert response.data["data"][1]["id"] == str(genre_drama.id)
        assert response.data["data"][1]["name"] == genre_drama.name
        assert response.data["data"][1]["is_active"] == genre_drama.is_active
        assert response.data["data"][1]["categories"] == []


@pytest.mark.django_db
class TestCreateAPI:
    def test_create_genre_with_categories_associated(
        self,
        category_repository,
        category_documentary,
        category_movie,
        genre_repository: DjangoORMGenreRepository,
    ):
        response = APIClient().post(
            "/api/genres/",
            data={
                "name": "Romance",
                "is_active": True,
                "categories": [str(category_movie.id), str(category_documentary.id)],
            },
        )

        assert response.status_code == 201
        assert response.data["id"]

        genre_saved = genre_repository.get_by_id(response.data["id"])
        assert genre_saved.name == "Romance"
        assert genre_saved.is_active is True
        assert genre_saved.categories == {category_movie.id, category_documentary.id}

    def test_create_genre_without_categories_associated(
        self, genre_repository: DjangoORMGenreRepository
    ):
        response = APIClient().post(
            "/api/genres/",
            data={
                "name": "Romance",
                "is_active": True,
                "categories": [],
            },
        )

        assert response.status_code == 201
        assert response.data["id"]

        genre_saved = genre_repository.get_by_id(response.data["id"])
        assert genre_saved.name == "Romance"
        assert genre_saved.is_active is True
        assert genre_saved.categories == set()

    def test_raise_error_when_genre_is_invalid(self):
        response = APIClient().post(
            "/api/genres/",
            data={
                "name": "",
                "is_active": True,
                "categories": [],
            },
        )

        assert response.status_code == 400
        assert response.data == {"name": ["This field may not be blank."]}


@pytest.mark.django_db
class TestDelete:
    def test_raise_when_id_not_valid(
        self,
    ):
        response = APIClient().delete("/api/genres/1/")

        assert response.status_code == 400

    def test_raise_when_genre_not_exists(self):
        response = APIClient().delete(f"/api/genres/{uuid.uuid4()}/")

        assert response.status_code == 404

    def test_delete_genre(self, genre_romance, genre_repository):
        genre_repository.save(genre_romance)

        assert GenreModel.objects.count() == 1

        response = APIClient().delete(f"/api/genres/{genre_romance.id}/")

        assert response.status_code == 204

        assert GenreModel.objects.count() == 0


@pytest.mark.django_db
class TestUpdatedAPI:
    def test_update_genre_with_categories_associated(
        self,
        category_repository,
        category_documentary,
        category_movie,
        genre_drama,
        genre_repository: DjangoORMGenreRepository,
    ):
        genre_repository.save(genre_drama)

        genre_saved = genre_repository.get_by_id(genre_drama.id)
        assert genre_saved.name == "Drama"
        assert genre_saved.is_active is True
        assert genre_saved.categories == set()

        response = APIClient().put(
            f"/api/genres/{genre_drama.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": "Drama updated",
                    "is_active": False,
                    "categories": [
                        str(category_movie.id),
                        str(category_documentary.id),
                    ],
                }
            ),
        )

        assert response.status_code == 204

        genre_updated = genre_repository.get_by_id(genre_drama.id)
        assert genre_updated.name == "Drama updated"
        assert genre_updated.is_active is False
        assert genre_updated.categories == {category_movie.id, category_documentary.id}

    def test_return_404_when_genre_not_exists(self):
        response = APIClient().put(
            f"/api/genres/{uuid.uuid4()}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": "Drama updated",
                    "is_active": False,
                    "categories": [],
                }
            ),
        )

        assert response.status_code == 404

    def test_return_400_when_payload_is_invalid(self):
        response = APIClient().put(
            f"/api/genres/{uuid.uuid4()}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": "",
                    "is_active": False,
                    "categories": [],
                }
            ),
        )

        assert response.status_code == 400
        assert response.data == {"name": ["This field may not be blank."]}
