import uuid

from src.core.genre.application.use_cases.exceptions import RelatedCategoriesNotFound
import pytest
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category import InMemoryCategoryRepository
from src.core.genre.application.use_cases.update_genre import (
    GenreUpdateRequest,
    UpdateGenre,
)
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre import InMemoryGenreRepository


class TestUpdateGenre:
    def test_update_genre_valid(self):
        repository = InMemoryGenreRepository()
        repository_category = InMemoryCategoryRepository([Category(name="category")])

        categories = repository_category.list()

        genre = Genre(name="genre", is_active=True, categories={categories[0].id})
        repository.save(genre)

        old_genre = repository.get_by_id(genre.id)

        assert old_genre.name == "genre"
        assert old_genre.is_active is True
        assert old_genre.categories == {categories[0].id}

        genre.name = "new genre"
        genre.is_active = False
        genre.categories = set()

        use_case = UpdateGenre(
            repository=repository, repository_category=repository_category
        )
        use_case.execute(
            GenreUpdateRequest(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
                categories=genre.categories,
            )
        )

        assert old_genre.name == "new genre"
        assert old_genre.is_active is False
        assert old_genre.categories == set()

    def test_raise_when_categorie_not_exist(self):
        repository = InMemoryGenreRepository()
        repository_category = InMemoryCategoryRepository()

        genre = Genre(name="genre", is_active=True, categories=set())
        repository.save(genre)

        use_case = UpdateGenre(
            repository=repository, repository_category=repository_category
        )

        with pytest.raises(RelatedCategoriesNotFound, match="Categories not found:"):
            use_case.execute(
                GenreUpdateRequest(
                    id=genre.id,
                    name="new genre",
                    is_active=False,
                    categories={uuid.uuid4()},
                )
            )

    def test_raise_when_name_is_not_valid(self):
        repository = InMemoryGenreRepository()
        repository_category = InMemoryCategoryRepository()

        genre = Genre(name="genre", is_active=True, categories=set())
        repository.save(genre)

        use_case = UpdateGenre(
            repository=repository, repository_category=repository_category
        )

        with pytest.raises(ValueError, match="Name is required"):
            use_case.execute(
                GenreUpdateRequest(
                    id=genre.id,
                    name="",
                    is_active=False,
                    categories=set(),
                )
            )
