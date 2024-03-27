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

        genre = Genre(name="genre", is_active=True)
        repository.save(genre)

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
        assert genre_saved.categories.all()[0].name == "category2"
        assert genre_saved.categories.all()[1].name == "category1"
