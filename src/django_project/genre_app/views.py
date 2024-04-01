from src.core.genre.application.use_cases.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.category_app.models import Category as CategoryModel
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.models import Genre as GenreModel
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.core.genre.application.use_cases.update_genre import (
    UpdateGenre,
    GenreUpdateRequest,
)
from src.core.genre.application.use_cases.delete_genre import (
    DeleteGenre,
    DeleteGenreRequest,
)
from src.core.genre.application.use_cases.create_genre import (
    CreateGenre,
    CreateGenreRequest,
)
from src.django_project.genre_app.serializers import (
    CreateGenreRequestSerializer,
    ListGenreResponseSerializer,
    CreateGenreResponseSerializer,
    DeleteGenreRequestSerializer,
    UpdateGenreRequestSerializer,
)


class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListGenre(repository=DjangoORMGenreRepository(GenreModel))

        response = use_case.execute()

        serializer = ListGenreResponseSerializer(instance=response)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request: Request) -> Response:
        serializer = CreateGenreRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            use_case = CreateGenre(
                repository_category=DjangoORMCategoryRepository(CategoryModel),
                repository=DjangoORMGenreRepository(GenreModel),
            )
            result = use_case.execute(
                request=CreateGenreRequest(**serializer.validated_data)
            )
            response = CreateGenreResponseSerializer(instance=result)
        except (InvalidGenre, RelatedCategoriesNotFound) as err:
            return Response(status=status.HTTP_404_NOT_FOUND, data=f"Error: {err}")

        return Response(status=status.HTTP_201_CREATED, data=response.data)

    def update(self, request: Request, pk=None) -> Response:
        serializer = UpdateGenreRequestSerializer(
            data={
                **request.data,
                "id": pk,
            }
        )
        serializer.is_valid(raise_exception=True)

        try:
            use_case = UpdateGenre(
                repository_category=DjangoORMCategoryRepository(
                    category_model=CategoryModel
                ),
                repository=DjangoORMGenreRepository(GenreModel),
            )
            use_case.execute(GenreUpdateRequest(**serializer.validated_data))
        except (GenreNotFound, RelatedCategoriesNotFound) as err:
            return Response(status=status.HTTP_404_NOT_FOUND, data=f"Error: {err}")

        return Response(
            status=status.HTTP_204_NO_CONTENT, data="Category updated successfully"
        )

    def destroy(self, request: Request, pk=None) -> Response:
        serializer = DeleteGenreRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        try:
            use_case = DeleteGenre(repository=DjangoORMGenreRepository(GenreModel))
            use_case.execute(DeleteGenreRequest(**serializer.validated_data))
        except GenreNotFound as err:
            return Response(status=status.HTTP_404_NOT_FOUND, data=f"{err}")

        return Response(
            status=status.HTTP_204_NO_CONTENT, data="Genre deleted successfully"
        )
