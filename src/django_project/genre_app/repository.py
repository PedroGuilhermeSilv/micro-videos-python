from django.db import transaction
from src.django_project.genre_app.models import Genre as GenreModel
from uuid import UUID
from src.core.genre.domain.genre import Genre
from src.core.genre.application.genre_repository import GenreRepository


class DjangoORMGenreRepository(GenreRepository):
    def __init__(self, genre_model: GenreModel):
        self.genre_model = genre_model

    def save(self, genre: Genre) -> None:
        with transaction.atomic():
            genre_model = self.genre_model.objects.create(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
            )
            genre_model.categories.set(genre.categories)

    def list(self) -> list[Genre]:
        return [
            Genre(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
                categories={category.id for category in genre.categories.all()},
            )
            for genre in self.genre_model.objects.all()
        ]

    def get_by_id(self, id: UUID) -> Genre | None:
        try:
            genre_model = self.genre_model.objects.get(id=id)
        except self.genre_model.DoesNotExist:
            return None
        return Genre(
            id=genre_model.id,
            name=genre_model.name,
            is_active=genre_model.is_active,
            categories={category.id for category in genre_model.categories.all()},
        )

    def update(self, genre: Genre) -> None:
        try:
            genre_model = self.genre_model.objects.get(id=genre.id)

        except self.genre_model.DoesNotExist:
            return None

        else:
            with transaction.atomic():
                self.genre_model.objects.filter(id=genre.id).update(
                    name=genre.name,
                    is_active=genre.is_active,
                )
                genre_model.categories.set(genre.categories)

    def delete(self, id: UUID) -> None:
        self.genre_model.objects.filter(id=id).delete()
