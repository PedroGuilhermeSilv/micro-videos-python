from src.core.category.application.use_cases.list_category import (
    ListCategory,
    ListCategoryRequest,
)
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django_project.category_app.repository import DjangoORMCategoryRespository
from django_project.category_app.models import Category as CategoryModel


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        dto_input = ListCategoryRequest()
        repository = DjangoORMCategoryRespository(CategoryModel)

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
