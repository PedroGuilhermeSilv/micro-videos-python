from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.models import Genre as GenreModel
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.django_project.genre_app.serializers import ListGenreResponseSerializer


class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListGenre(repository=DjangoORMGenreRepository(GenreModel))

        response = use_case.execute()

        serializer = ListGenreResponseSerializer(instance=response)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    # def retrieve(self, request: Request, pk=None) -> Response:
    #     serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
    #     serializer.is_valid(raise_exception=True)
    #     category_id = serializer.validated_data["id"]

    #     try:
    #         use_case = GetCategory(
    #             repository=DjangoORMCategoryRepository(CategoryModel)
    #         )
    #         result = use_case.execute(CategoryGetRequest(id=category_id))
    #     except CategoryNotFound:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    #     serializer = RetrieveCategoryResponseSerializer(instance=result)
    #     response = serializer.data

    #     return Response(status=status.HTTP_200_OK, data=response)

    # def create(self, request: Request) -> Response:
    #     serializer = CreateCategoryRequestSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     try:
    #         use_case = CreateCategory(
    #             repository=DjangoORMCategoryRepository(category_model=CategoryModel)
    #         )
    #         result = use_case.execute(
    #             CategoryCreateRequest(**serializer.validated_data)
    #         )
    #         response = CreateCategoryResponseSerializer(instance=result)
    #     except CategoryNotFound:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    #     return Response(status=status.HTTP_201_CREATED, data=response.data)

    # def update(self, request: Request, pk=None) -> Response:
    #     serializer = UpdateCategoryRequestSerializer(
    #         data={
    #             **request.data,
    #             "id": pk,
    #         }
    #     )
    #     serializer.is_valid(raise_exception=True)

    #     try:
    #         use_case = UpdateCategory(
    #             repository=DjangoORMCategoryRepository(category_model=CategoryModel)
    #         )
    #         use_case.execute(CategoryUpdateRequest(**serializer.validated_data))
    #     except CategoryNotFound:
    #         return Response(status=status.HTTP_404_NOT_FOUND, data="Category not found")

    #     return Response(
    #         status=status.HTTP_204_NO_CONTENT, data="Category updated successfully"
    #     )

    # def delete(self, request: Request, pk=None) -> Response:
    #     serializer = DeleteCategoryRequestSerializer(data={"id": pk})
    #     serializer.is_valid(raise_exception=True)

    #     try:
    #         use_case = DeleteCategory(
    #             repository=DjangoORMCategoryRepository(category_model=CategoryModel)
    #         )
    #         use_case.execute(DeleteCategoryRequest(id=serializer.validated_data["id"]))
    #     except CategoryNotFound:
    #         return Response(status=status.HTTP_404_NOT_FOUND, data="Category not found")

    #     return Response(
    #         status=status.HTTP_204_NO_CONTENT, data="Category deleted successfully"
    #     )
