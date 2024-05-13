import uuid
from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.category_app.models import Category as CategoryModel
import pytest


@pytest.mark.django_db
class TestSave:
    def test_save_category_in_database(self):
        category = Category(
            name="Category 1",
            description="Category 1 description",
            is_active=True,
        )
        repository = DjangoORMCategoryRepository(CategoryModel)
        assert CategoryModel.objects.count() == 0

        repository.save(category)

        assert CategoryModel.objects.count() == 1
        category_db = CategoryModel.objects.first()
        assert category_db.name == "Category 1"
        assert category_db.description == "Category 1 description"
        assert category_db.is_active is True


@pytest.mark.django_db
class TestGetById:
    def test_get_category_by_id(self):
        category = Category(
            name="Category 1",
            description="Category 1 description",
            is_active=True,
        )
        repository = DjangoORMCategoryRepository(CategoryModel)
        category_orm = CategoryModel.objects.create(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

        category_db = repository.get_by_id(category_orm.id)

        assert category_db.id == category_orm.id
        assert category_db.name == category_orm.name
        assert category_db.description == category_orm.description
        assert category_db.is_active == category_orm.is_active

    def test_get_category_by_id_not_found(self):
        id_not_found = uuid.uuid4()
        repository = DjangoORMCategoryRepository(CategoryModel)
        category_db = repository.get_by_id(id=id_not_found)

        assert category_db is None


@pytest.mark.django_db
class TestDelete:
    def test_delete_category_by_id(self):
        category = Category(
            name="Category 1",
            description="Category 1 description",
            is_active=True,
        )
        repository = DjangoORMCategoryRepository(CategoryModel)
        category_orm = CategoryModel.objects.create(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

        assert CategoryModel.objects.count() == 1

        repository.delete(category_orm.id)

        assert CategoryModel.objects.count() == 0


@pytest.mark.django_db
class TestList:
    def test_list_categories(self):
        category_1 = Category(
            name="Category 1",
            description="Category 1 description",
            is_active=True,
        )
        category_2 = Category(
            name="Category 2",
            description="Category 2 description",
            is_active=True,
        )
        repository = DjangoORMCategoryRepository(CategoryModel)
        category_orm_1 = CategoryModel.objects.create(
            name=category_1.name,
            description=category_1.description,
            is_active=category_1.is_active,
        )
        category_orm_2 = CategoryModel.objects.create(
            name=category_2.name,
            description=category_2.description,
            is_active=category_2.is_active,
        )

        categories = repository.list()

        assert len(categories) == 2
        assert categories[0].id == category_orm_1.id
        assert categories[0].name == category_orm_1.name
        assert categories[0].description == category_orm_1.description
        assert categories[0].is_active == category_orm_1.is_active
        assert categories[1].id == category_orm_2.id
        assert categories[1].name == category_orm_2.name
        assert categories[1].description == category_orm_2.description
        assert categories[1].is_active == category_orm_2.is_active


@pytest.mark.django_db
class TestUpdate:
    def test_update_category(self):
        category = Category(
            name="Category 1",
            description="Category 1 description",
            is_active=True,
        )
        repository = DjangoORMCategoryRepository(CategoryModel)

        repository.save(category)
        category_db = repository.get_by_id(category.id)
        assert category_db.name == "Category 1"
        assert category_db.description == "Category 1 description"
        assert category_db.is_active is True
        assert CategoryModel.objects.count() == 1

        category.name = "Category 1 Updated"
        category.description = "Category 1 description updated"
        category.is_active = False
        repository.update(category)

        category_db = repository.get_by_id(category_db.id)
        assert category_db.name == "Category 1 Updated"
        assert category_db.description == "Category 1 description updated"
        assert category_db.is_active is False
