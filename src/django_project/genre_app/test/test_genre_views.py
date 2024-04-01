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
        # assert response.data == expected_response
