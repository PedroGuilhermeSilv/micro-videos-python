import uuid
from src.core.genre.domain.genre import Genre
import pytest


class TestCreateGenre:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument"):
            Genre()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="Name must have less than 255 characters"):
            Genre("a" * 256)

    def test_create_category_with_all_values(self):
        genre = Genre(name="Romance", is_active=False, categories={uuid.uuid4()})
        assert genre.name == "Romance"
        assert genre.is_active is False
        assert isinstance(genre.id, uuid.UUID)
        assert isinstance(genre.categories, set)
        assert len(genre.categories) == 1

    def test_cannot_create_genre_with_name_empty(self):
        with pytest.raises(ValueError, match="Name is required"):
            Genre(name="")

    def test_str_is_correct(self):
        genre = Genre(name="Romance", is_active=True)
        assert str(genre) == "Genre: Romance - True"


class TestChangeNameGenre:
    def test_change_name_valid(self):
        genre = Genre(name="Romance")
        genre.change_name("Action")
        assert genre.name == "Action"

    def test_change_name_empty(self):
        genre = Genre(name="Romance")
        with pytest.raises(ValueError, match="Name is required"):
            genre.change_name("")


class TestActiveGenre:
    def test_active_genre_inactive(self):
        genre = Genre(name="Romance", is_active=False)
        genre.activate()
        assert genre.is_active is True

    def test_active_genre_active(self):
        genre = Genre(name="Romance")
        genre.activate()
        assert genre.is_active is True


class TestDeactivateGenre:
    def test_deactivate_genre_active(self):
        genre = Genre(name="Romance")
        genre.deactivate()
        assert genre.is_active is False

    def test_deactivate_genre_inactive(self):
        genre = Genre(name="Romance", is_active=False)
        genre.deactivate()
        assert genre.is_active is False


class TestEquality:
    def test_genre_id_equals(self):
        common_id = uuid.uuid4()
        genre = Genre(name="Romance", id=common_id)
        other_genre = Genre(name="Romance", id=common_id)
        assert genre == other_genre

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        genre = Genre(name="Romance", id=common_id)
        dummy = Dummy()
        dummy.id = common_id
        with pytest.raises(ValueError, match="Comparison between different classes"):
            genre == dummy
