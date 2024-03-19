from uuid import UUID
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import (
    CategoryGetRequest,
    GetCategory,
)
from src.core.category.application.use_cases.list_category import (
    ListCategory,
    ListCategoryRequest,
)
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.models import Category as CategoryModel


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        dto_input = ListCategoryRequest()
        repository = DjangoORMCategoryRepository(CategoryModel)

        use_case = ListCategory(repository=repository)
        output = use_case.execute(dto_input)
        categories = [
            {
                "id": str(category.id),
                "name": category.name,
                "description": category.description,
                "is_active": category.is_active,
            }
            for category in output.data
        ]

        return Response(status=status.HTTP_200_OK, data=categories)

    def retrieve(self, request: Request, pk=None) -> Response:
        try:
            category_id = UUID(pk)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            repository = DjangoORMCategoryRepository(CategoryModel)
            use_case = GetCategory(repository=repository)
            category = use_case.execute(CategoryGetRequest(id=category_id))

            response = {
                "id": str(category.id),
                "name": category.name,
                "description": category.description,
                "is_active": category.is_active,
            }

        except CategoryNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK, data=response)
