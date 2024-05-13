import uuid
from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository
import pytest
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.models import Genre as GenreModel
from src.django_project.category_app.models import Category as CategoryModel
from src.core.genre.domain.genre import Genre


@pytest.mark.django_db
class TestSave:
    def test_save_genre_in_database(self):
        repository = DjangoORMGenreRepository(genre_model=GenreModel)

        assert GenreModel.objects.count() == 0

        repository.save(Genre(name="genre", is_active=True))

        genre_saved = GenreModel.objects.first()

        assert GenreModel.objects.count() == 1
        assert genre_saved.name == "genre"
        assert genre_saved.is_active is True

    def test_save_genre_with_categories(self):
        repository = DjangoORMGenreRepository(genre_model=GenreModel)
        repository_category = DjangoORMCategoryRepository(category_model=CategoryModel)

        repository_category.save(Category(name="category1"))
        repository_category.save(Category(name="category2"))

        assert CategoryModel.objects.count() == 2

        categories_id = CategoryModel.objects.values_list("id", flat=True)
        genre = Genre(
            name="genre",
            is_active=True,
            categories={categories_id[0], categories_id[1]},
        )

        repository.save(genre)

        genre_saved = GenreModel.objects.first()

        assert GenreModel.objects.count() == 1
        assert genre_saved.categories.count() == 2
        assert genre_saved.categories.all()[0].name == "category1"
        assert genre_saved.categories.all()[1].name == "category2"


@pytest.mark.django_db
class TestGetById:
    def test_get_genre_by_id(self):
        genre = Genre(
            name="Movie",
            is_active=True,
        )
        repository = DjangoORMGenreRepository(GenreModel)
        genre_orm = GenreModel.objects.create(
            name=genre.name,
            is_active=genre.is_active,
        )

        genre_db = repository.get_by_id(genre_orm.id)

        assert genre_db.id == genre_orm.id
        assert genre_db.name == genre_orm.name
        assert genre_db.is_active == genre_orm.is_active

    def test_get_genre_by_id_not_found(self):
        id_not_found = uuid.uuid4()
        repository = DjangoORMGenreRepository(GenreModel)
        genre_db = repository.get_by_id(id=id_not_found)

        assert genre_db is None


@pytest.mark.django_db
class TestDelete:
    def test_delete_genre_by_id(self):
        genre = Genre(
            name="Movie",
            is_active=True,
        )
        repository = DjangoORMGenreRepository(GenreModel)
        genre_orm = GenreModel.objects.create(
            name=genre.name,
            is_active=genre.is_active,
        )

        assert GenreModel.objects.count() == 1

        repository.delete(genre_orm.id)

        assert GenreModel.objects.count() == 0


@pytest.mark.django_db
class TestList:
    def test_list_genres(self):
        genre1 = Genre(
            name="Movie",
            is_active=True,
        )
        genre2 = Genre(
            name="Series",
            is_active=True,
        )
        repository = DjangoORMGenreRepository(GenreModel)
        genre_orm_1 = GenreModel.objects.create(
            name=genre1.name,
            is_active=genre1.is_active,
        )
        genre_orm_2 = GenreModel.objects.create(
            name=genre2.name,
            is_active=genre2.is_active,
        )

        genres = repository.list()

        assert len(genres) == 2
        assert genres[0].id == genre_orm_1.id
        assert genres[0].name == genre_orm_1.name
        assert genres[0].is_active == genre_orm_1.is_active
        assert genres[1].id == genre_orm_2.id
        assert genres[1].name == genre_orm_2.name
        assert genres[1].is_active == genre_orm_2.is_active


@pytest.mark.django_db
class TestUpdate:
    def test_update_genre(self):
        genre = Genre(
            name="Genre 1",
            is_active=True,
        )

        repository = DjangoORMGenreRepository(GenreModel)

        repository.save(genre)
        genre_db = repository.get_by_id(genre.id)
        assert genre_db.name == "Genre 1"
        assert genre_db.is_active is True
        assert GenreModel.objects.count() == 1

        genre.name = "Genre 1 Updated"
        genre.is_active = False
        repository.update(genre)

        genre_db = repository.get_by_id(genre.id)
        assert genre_db.name == "Genre 1 Updated"
        assert genre_db.is_active is False
